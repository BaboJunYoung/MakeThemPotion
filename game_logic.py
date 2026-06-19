"""Potion Workshop - 순수 게임 로직 (pygame 의존성 없음).

이 모듈은 렌더링/입력과 완전히 분리되어 있어 test.py 에서 독립적으로,
빠르고 안전하게 디버깅할 수 있다. main.py 는 GameState 를 호출하기만 한다.
"""

import random


# ---------------------------------------------------------------------------
# 데이터
# ---------------------------------------------------------------------------

# 재료 10종. image 는 아이콘 파일명, color 는 폴백 색.
# === 불법 재료 리스크 시스템 ===
#   suspicious=False : 정상 재료. 수입(reward)은 적고 검사 위험(risk)은 없다.
#   suspicious=True  : 수상한(불법) 재료. 수입은 크지만 검사 게이지(risk)가 오른다.
INGREDIENTS = [
    {"id": "grape", "name": "포도", "image": "포도.png", "color": (128, 80, 170),
     "suspicious": False, "reward": 3, "risk": 0},
    {"id": "ddungi", "name": "뚱이", "image": "뚱이.png", "color": (240, 150, 160),
     "suspicious": False, "reward": 3, "risk": 0},
    {"id": "pupa", "name": "번데기", "image": "번데기.png", "color": (150, 110, 70),
     "suspicious": False, "reward": 3, "risk": 0},
    {"id": "wing", "name": "나비날개", "image": "나비날개.png", "color": (150, 200, 230),
     "suspicious": False, "reward": 3, "risk": 0},
    {"id": "tomato", "name": "불타는도마도", "image": "불타는도마도.png", "color": (220, 80, 60),
     "suspicious": False, "reward": 4, "risk": 0},
    {"id": "ginseng", "name": "산삼", "image": "산삼.png", "color": (200, 180, 120),
     "suspicious": False, "reward": 5, "risk": 0},
    {"id": "acorn", "name": "도토링", "image": "도토링.png", "color": (160, 120, 70),
     "suspicious": False, "reward": 3, "risk": 0},
    # --- 수상한(불법) 재료: 고수익·고위험 ---
    {"id": "smurf", "name": "갈린스머프", "image": "갈린스머프.png", "color": (90, 140, 210),
     "suspicious": True, "reward": 20, "risk": 18},
    {"id": "eyeball", "name": "눈알", "image": "눈알.png", "color": (225, 225, 225),
     "suspicious": True, "reward": 20, "risk": 18},
    {"id": "stone", "name": "요로결석", "image": "요로결석.png", "color": (205, 195, 155),
     "suspicious": True, "reward": 24, "risk": 22},
]

# 레시피 15종. 각 포션은 재료 2~3개 조합으로 만든다 (순서 무관).
RECIPES = [
    {"potion_id": "healing", "name": "회복 포션",
     "ingredients": ["ginseng", "grape"], "color": (232, 77, 91)},
    {"potion_id": "strength", "name": "힘 포션",
     "ingredients": ["tomato", "ginseng"], "color": (242, 153, 74)},
    {"potion_id": "sleep", "name": "수면 포션",
     "ingredients": ["pupa", "acorn"], "color": (53, 79, 140)},
    {"potion_id": "luck", "name": "행운 포션",
     "ingredients": ["wing", "grape"], "color": (242, 201, 76)},
    {"potion_id": "invisible", "name": "투명 포션",
     "ingredients": ["wing", "smurf"], "color": (150, 200, 230)},
    {"potion_id": "madness", "name": "광기 포션",
     "ingredients": ["eyeball", "tomato"], "color": (180, 60, 140)},
    {"potion_id": "fire", "name": "화염 포션",
     "ingredients": ["tomato", "ddungi"], "color": (230, 90, 40)},
    {"potion_id": "poison", "name": "맹독 포션",
     "ingredients": ["stone", "eyeball"], "color": (110, 170, 70)},
    {"potion_id": "flight", "name": "비행 포션",
     "ingredients": ["wing", "pupa"], "color": (120, 200, 200)},
    {"potion_id": "giant", "name": "거인 포션",
     "ingredients": ["ddungi", "ginseng"], "color": (180, 120, 80)},
    {"potion_id": "wisdom", "name": "지혜 포션",
     "ingredients": ["acorn", "eyeball"], "color": (90, 160, 200)},
    {"potion_id": "charm", "name": "매혹 포션",
     "ingredients": ["grape", "smurf"], "color": (210, 110, 190)},
    {"potion_id": "shield", "name": "방어 포션",
     "ingredients": ["stone", "acorn"], "color": (150, 150, 170)},
    {"potion_id": "haste", "name": "신속 포션",
     "ingredients": ["smurf", "acorn", "pupa"], "color": (240, 220, 90)},
    {"potion_id": "legendary", "name": "전설 포션",
     "ingredients": ["ginseng", "wing", "eyeball"], "color": (255, 215, 120)},
]

FAILED_POTION = {
    "potion_id": "failed",
    "name": "수상한 포션",
    "ingredients": [],
    "color": (123, 114, 128),
}

CUSTOMERS = [
    {"id": "novice_adventurer", "name": "초보 모험가", "orders": ["healing", "strength"]},
    {"id": "sleepy_student", "name": "졸린 마법 학생", "orders": ["sleep", "wisdom"]},
    {"id": "unlucky_merchant", "name": "운 없는 상인", "orders": ["luck", "charm"]},
    {"id": "timid_knight", "name": "겁 많은 기사", "orders": ["strength", "shield"]},
    {"id": "tired_miner", "name": "일하는 광부", "orders": ["strength", "healing", "giant"]},
    {"id": "suspicious_visitor", "name": "수상한 손님", "orders": ["poison", "madness"]},
]

# 포션별 주문 대사. 모든 포션은 최소 한 줄을 가진다.
ORDER_LINES = {
    "healing": ["온몸이 욱신거려요. 상처가 빨리 낫는 약이 필요해요.",
                "던전에서 구른 것 같아요. 회복시켜 주세요."],
    "strength": ["오늘 큰 바위를 치워야 해요. 힘이 솟는 약 주세요.",
                 "무거운 짐을 산처럼 옮겨야 합니다. 힘이 필요해요."],
    "sleep": ["요즘 통 잠을 못 자요. 깊은 잠이 필요해요.",
              "옆집 폭발 실험 때문에 한숨도 못 잤어요."],
    "luck": ["오늘 중요한 주사위 승부가 있어요. 운이 필요합니다.",
             "고백하러 가는데, 성공 확률을 올리고 싶어요."],
    "invisible": ["몰래 빠져나가야 할 일이 있어요. 모습을 감추고 싶어요.",
                  "잠깐 투명해지는 약이 있을까요?"],
    "madness": ["적을 혼란에 빠뜨릴 약이 필요해요.",
                "정신을 어지럽히는 광기의 약을 주세요."],
    "fire": ["불꽃을 다루는 약이 필요해요. 뜨겁게요!",
             "추운 북쪽으로 가요. 몸을 태울 듯 데워 주세요."],
    "poison": ["조용히 처리할 일이 있어요... 맹독 한 병이요.",
               "쥐가 들끓어요. 아주 독한 약이 필요합니다."],
    "flight": ["하늘을 날아 산을 넘어야 해요. 비행 약 주세요.",
               "발이 땅에 닿지 않는 약이 있나요?"],
    "giant": ["거인처럼 커지는 약이 필요해요.",
              "성문을 밀어야 해요. 몸집을 키워 주세요."],
    "wisdom": ["내일 마법 시험이에요. 지혜의 약이 필요해요.",
               "머리가 맑아지는 약 있나요?"],
    "charm": ["사교 모임에 가요. 매혹적으로 보이고 싶어요.",
              "마음을 사로잡는 약을 주세요."],
    "shield": ["전장에 나가요. 몸을 단단히 지켜 줄 약이요.",
               "화살이 빗발쳐요. 방어 약이 필요합니다."],
    "haste": ["경주가 있어요. 번개처럼 빨라지고 싶어요.",
              "시간이 없어요! 신속의 약 주세요."],
    "legendary": ["전설의 포션을 만들 수 있나요? 최고급으로요.",
                  "왕께 바칠 약이에요. 가장 귀한 걸로 주세요."],
}

# Day 1 첫 손님 전용 튜토리얼 대사 (매우 직접적)
TUTORIAL_LINES = {
    "healing": "다쳐서 회복할 약이 필요해요. 생기 있어 보이는 재료가 좋겠죠?",
    "strength": "힘이 솟는 약이 필요해요. 단단하고 강한 재료를 넣어 주세요.",
}

CORRECT_REACTIONS = [
    "완벽해요! 딱 필요하던 거예요.",
    "역시 이 가게는 믿을 만하군요.",
    "효과가 벌써 느껴지는 것 같아요.",
    "다음에도 여기로 올게요.",
]

WRONG_REACTIONS = [
    "음... 제가 원한 효과는 아닌 것 같은데요.",
    "이걸 마셔도 괜찮은 거 맞나요?",
    "조금 불안하지만... 일단 가져가 볼게요.",
    "다음엔 주문을 더 또렷하게 말해야겠네요.",
]

# 하루 진행 설정: 손님 수, 등장 포션, 목표 골드. 날이 갈수록 포션 종류가 늘어난다.
DAY_CONFIG = {
    1: {"customers": 3, "potions": ["healing", "strength"], "goal": 20},
    2: {"customers": 4, "potions": ["healing", "strength", "sleep", "luck"], "goal": 30},
    3: {"customers": 5,
        "potions": ["healing", "strength", "sleep", "luck", "fire", "poison", "flight"],
        "goal": 40},
}
# Day 4+ 공통 설정: 15종 전체 랜덤 등장
DAY_DEFAULT = {"customers": 5, "potions": [r["potion_id"] for r in RECIPES], "goal": 50}

# 이 날까지 모두 성공하면 게임 클리어(성공 화면).
FINAL_DAY = 3

REWARD_CORRECT = 10
REWARD_WRONG = 2

# 재료는 최소 2개, 최대 3개까지 넣어 조합한다.
MIN_INGREDIENTS = 2
MAX_INGREDIENTS = 3

# ===========================================================================
# 경영 모드 시스템 (발표용 차별화 요소) — 아래 4개 시스템이 핵심 차별점이다.
# ===========================================================================

# === 월세 목표 시스템 ===
# 제한 시간 안에 money(=gold)를 rent_goal 이상으로 모아야 가게를 지킨다.
# 정상 재료만 팔아서는 절대 못 갚을 만큼 목표를 크게 잡아 위험을 강요한다.
RENT_GOAL = 300
GAME_TIME_LIMIT = 120.0      # 제한 시간(초)

# === 불법 재료 리스크 시스템 ===
CORRECT_BONUS = 8            # 주문을 맞히면 주는 기본 수입
WRONG_INSPECTION = 12       # 주문을 틀리면 오르는 검사 게이지
PENALTY_WRONG = 15          # 요청을 틀리면 빼앗기는 돈 (음수가 되면 즉시 적발)
SUSPICION_LEAK = 0.06       # 불법 재료 누적분이 시간이 지나며 새는 양(결제 내역 추적)

# === 한울 검사 게이지 ===
INSPECTION_MAX = 100        # 게이지 상한
HANUL_INTERVAL = 38.0       # 이 시간(초)마다 한울이가 검사하러 등장
HANUL_TRIGGER_GAUGE = 60    # 게이지가 이 이상이면 즉시 등장
HANUL_RISE_RATE = 6.0       # 검사 중일 때 게이지 상승 속도(초당)
HANUL_WINDOW = 15.0         # 한울 검사 제한 시간(초). 안에 퇴치 못 하면 적발
HANUL_VERIFY_AT = 10.0      # 이 시간(초)이 지나면 '의심' → '검증' 단계

# === 퇴치 포션 시스템 ===
REPEL_RELIEF = 35           # 퇴치 성공 시 내려가는 검사 게이지
# 후반엔 한울이가 내성이 생겨 더 강한 조합이 필요하다 (early → late 로 강화).
REPEL_RECIPES = {
    "early": [["eyeball", "grape"]],              # 수상한 버섯 + 물 컨셉
    "late": [["eyeball", "stone", "smurf"]],      # 수상한 버섯 + 정체불명 가루 + 렌몬 시럽 컨셉
}

# 페이즈 상수
PHASE_ORDER = "order"        # 손님 주문 표시 / 재료 선택 대기
PHASE_BREWING = "brewing"    # 재료 선택 중
PHASE_CRAFTED = "crafted"    # 포션 완성, 제출 대기
PHASE_RESULT = "result"      # 제출 결과 표시
PHASE_DAY_END = "day_end"    # 하루 정산
PHASE_GAME_OVER = "game_over"  # 월세 성공/실패/적발 엔딩


# ---------------------------------------------------------------------------
# 순수 함수
# ---------------------------------------------------------------------------

def get_ingredient(ingredient_id):
    for ing in INGREDIENTS:
        if ing["id"] == ingredient_id:
            return ing
    return None


def get_recipe(potion_id):
    for recipe in RECIPES:
        if recipe["potion_id"] == potion_id:
            return recipe
    return None


def get_potion_by_ingredients(selected_ingredients):
    """재료 2~3개 조합으로 포션을 판정한다. 순서 무관. 매칭 실패 시 수상한 포션."""
    sorted_selected = sorted(selected_ingredients)
    for recipe in RECIPES:
        if sorted(recipe["ingredients"]) == sorted_selected:
            return dict(recipe)
    result = dict(FAILED_POTION)
    result["ingredients"] = list(selected_ingredients)
    return result


def get_day_config(day):
    return DAY_CONFIG.get(day, DAY_DEFAULT)


def _pick_customer_for_potion(potion_id, rng):
    """해당 포션을 주문할 법한 손님 유형을 고른다. 없으면 아무나."""
    matching = [c for c in CUSTOMERS if potion_id in c["orders"]]
    pool = matching if matching else CUSTOMERS
    return rng.choice(pool)


def generate_day_customers(day, rng):
    """하루치 손님 목록을 생성한다. 각 항목은 손님/목표포션/주문대사를 포함한다."""
    config = get_day_config(day)
    count = config["customers"]
    available = config["potions"]
    customers = []

    for index in range(count):
        # Day 1 첫 손님은 가장 쉬운 회복 포션 튜토리얼로 고정.
        if day == 1 and index == 0:
            target = "healing"
            line = TUTORIAL_LINES[target]
        elif day == 1 and index == 1:
            target = "strength"
            line = TUTORIAL_LINES[target]
        else:
            target = rng.choice(available)
            line = rng.choice(ORDER_LINES[target])

        customer = _pick_customer_for_potion(target, rng)
        customers.append({
            "customer": customer,
            "target_potion": target,
            "order_line": line,
        })
    return customers


def evaluate(crafted_potion_id, target_potion_id):
    """제출 결과를 평가한다. (정답여부, 골드) 반환."""
    correct = (crafted_potion_id == target_potion_id and crafted_potion_id != "failed")
    gold = REWARD_CORRECT if correct else REWARD_WRONG
    return correct, gold


# ---------------------------------------------------------------------------
# 손님 대기 스택 (프로젝트 조건: LIFO 스택 구조)
# ---------------------------------------------------------------------------

class CustomerStack:
    """손님 대기 스택.

    generate_day_customers() 결과를 역순으로 쌓아 pop() 시 원래 순서(튜토리얼
    고정 포함)대로 손님이 나오게 한다.
    """

    def __init__(self, customers):
        # 첫 손님이 꼭대기에 오도록 역순 push
        self._data = list(reversed(customers))

    def peek(self):
        """꼭대기 손님을 반환 (꺼내지 않음)."""
        return self._data[-1] if self._data else None

    def pop(self):
        """꼭대기 손님을 꺼낸다."""
        return self._data.pop() if self._data else None

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return not self._data


# ---------------------------------------------------------------------------
# 게임 상태 (전체 흐름 관리, 렌더링 없음)
# ---------------------------------------------------------------------------

class GameState:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.day = 1
        self.gold = 0          # 누적 총 골드 = money (상단 표시)

        # === 월세 목표 시스템 / 제한 시간 ===
        self.rent_goal = RENT_GOAL
        self.time_left = GAME_TIME_LIMIT
        # === 한울 검사 게이지 ===
        self.inspection_gauge = 0.0
        self.illegal_used = 0          # 지금까지 판매에 쓴 불법 재료 수(결제 내역 추적용)
        # === 퇴치 포션 시스템 / 한울 등장 ===
        self.hanul_active = False
        self.hanul_level = "early"     # early → late (내성)
        self.hanul_timer = 0.0         # 다음 등장까지 경과 시간
        self.hanul_time_left = 0.0     # 검사 중 남은 제한 시간(의심/검증)
        self.repel_message = ""        # 한울 등장/퇴치 안내 문구
        self.caught_reason = ""        # 적발 사유 (게임오버 화면 표시)
        self.ending = None             # None / "clear" / "rent_fail" / "busted"

        self.start_day()

    # --- 하루 시작 ---------------------------------------------------------
    def start_day(self):
        customers = generate_day_customers(self.day, self.rng)
        self.customer_stack = CustomerStack(customers)
        self._total_customers = len(customers)
        self._served = 0
        self.gold_today = 0
        self.day_success = False
        self._reset_brewing()
        self.phase = PHASE_ORDER
        self.last_result = None  # {"correct", "gold", "reaction", "potion"}

    def _reset_brewing(self):
        self.selected = []
        self.crafted_potion = None

    # --- 조회 --------------------------------------------------------------
    @property
    def goal(self):
        return get_day_config(self.day)["goal"]

    @property
    def total_customers(self):
        return self._total_customers

    @property
    def current_index(self):
        """현재까지 응대한 손님 수 (이미지/이름 선택 기준)."""
        return self._served

    @property
    def current_customer(self):
        return self.customer_stack.peek()

    def can_craft(self):
        return (self.phase in (PHASE_ORDER, PHASE_BREWING)
                and MIN_INGREDIENTS <= len(self.selected) <= MAX_INGREDIENTS)

    def can_submit(self):
        return self.phase == PHASE_CRAFTED and self.crafted_potion is not None

    # --- 행동 --------------------------------------------------------------
    def add_ingredient(self, ingredient_id):
        """재료를 가마솥에 추가. 최대 2개, 중복 불가. 성공 시 True."""
        if self.phase not in (PHASE_ORDER, PHASE_BREWING):
            return False
        if len(self.selected) >= MAX_INGREDIENTS:
            return False
        if ingredient_id in self.selected:
            return False
        if get_ingredient(ingredient_id) is None:
            return False
        self.selected.append(ingredient_id)
        self.phase = PHASE_BREWING
        return True

    def clear_ingredients(self):
        """가마솥 비우기 (제작 전까지만 허용)."""
        if self.phase in (PHASE_ORDER, PHASE_BREWING, PHASE_CRAFTED):
            self._reset_brewing()
            self.phase = PHASE_ORDER
            return True
        return False

    def remove_ingredient(self, ingredient_id):
        """선택한 재료 하나를 취소(제거)한다. 제작된 상태면 제작을 되돌린다."""
        if self.phase not in (PHASE_ORDER, PHASE_BREWING, PHASE_CRAFTED):
            return False
        if ingredient_id not in self.selected:
            return False
        self.selected.remove(ingredient_id)
        self.crafted_potion = None
        self.phase = PHASE_BREWING if self.selected else PHASE_ORDER
        return True

    def _repel_match(self, selected, level):
        want = sorted(selected)
        return any(sorted(r) == want for r in REPEL_RECIPES.get(level, []))

    def craft(self):
        """선택한 재료 2~3개로 포션 제작."""
        if not self.can_craft():
            return False
        # === 퇴치 포션 시스템: 한울 검사 중 알맞은 퇴치 레시피면 쫓아낸다 ===
        if self.hanul_active:
            if self._repel_match(self.selected, self.hanul_level):
                self.inspection_gauge = max(0.0, self.inspection_gauge - REPEL_RELIEF)
                self.hanul_active = False
                self.hanul_timer = 0.0
                self.hanul_time_left = 0.0
                if self.hanul_level == "early":
                    self.hanul_level = "late"   # 한울이가 내성이 생긴다
                self.repel_message = "퇴치 포션 성공! 한울이가 잠시 물러갔다."
                self._reset_brewing()
                self.phase = PHASE_ORDER
                return True
            # 다른 단계의 퇴치 레시피를 만들면 내성 안내 (후반엔 초반 레시피 무효)
            if self._repel_match(self.selected, "early") or self._repel_match(self.selected, "late"):
                self.repel_message = "한울이가 내성이 생겼다! 더 강한 퇴치 포션이 필요해."
        self.crafted_potion = get_potion_by_ingredients(self.selected)
        self.phase = PHASE_CRAFTED
        return True

    def submit(self):
        """완성 포션을 현재 손님에게 제출하고 보상 처리."""
        if not self.can_submit():
            return False
        target = self.current_customer["target_potion"]
        correct, _ = evaluate(self.crafted_potion["potion_id"], target)

        # === 불법 재료 리스크 시스템 ===
        # 손님 수입은 주문을 맞혔을 때만 재료값까지 받는다(틀리면 소액).
        # 검사 위험(risk)은 불법 재료를 쓴 이상 정답/오답과 무관하게 오른다.
        ingredients = self.crafted_potion.get("ingredients", [])
        risk = 0 if correct else WRONG_INSPECTION   # 주문을 틀려도 의심을 산다
        suspicious_count = 0
        ingredient_reward = 0
        for iid in ingredients:
            ing = get_ingredient(iid)
            if not ing:
                continue
            ingredient_reward += ing["reward"]
            risk += ing["risk"]
            if ing["suspicious"]:
                suspicious_count += 1
        # 주문을 맞히면 재료값까지 받고, 틀리면 돈을 빼앗긴다(음수면 tick 에서 즉시 적발).
        reward = (CORRECT_BONUS + ingredient_reward) if correct else -PENALTY_WRONG

        self.gold += reward
        self.gold_today += reward
        # === 한울 검사 게이지 상승 ===
        self.inspection_gauge = min(INSPECTION_MAX, self.inspection_gauge + risk)
        self.illegal_used += suspicious_count

        reactions = CORRECT_REACTIONS if correct else WRONG_REACTIONS
        self.last_result = {
            "correct": correct,
            "gold": reward,
            "reaction": self.rng.choice(reactions),
            "potion": self.crafted_potion,
            "suspicious": suspicious_count,
        }
        self.phase = PHASE_RESULT
        return True

    def trigger_busted(self, reason):
        """한울이에게 적발되어 게임오버 ("한울이한테적발")."""
        self.caught_reason = reason
        self.hanul_active = False
        self.phase = PHASE_GAME_OVER
        self.ending = "busted"

    def tick(self, dt):
        """제한 시간·검사 게이지·한울 검사를 시간에 따라 갱신한다 (main 루프가 매 프레임 호출).

        결과/정산/엔딩 화면에서는 시간이 멈춰 플레이어가 읽을 여유를 준다.
        단, 자금이 음수가 되면 어느 화면에서든 즉시 적발된다.
        """
        if self.ending is not None:
            return
        # === 자금 마이너스 → 즉시 "한울이한테적발" ===
        if self.gold < 0:
            self.trigger_busted("자금이 바닥나 빚을 들켰다")
            return
        if self.phase not in (PHASE_ORDER, PHASE_BREWING, PHASE_CRAFTED):
            return

        # === 제한 시간 시스템 ===
        self.time_left = max(0.0, self.time_left - dt)
        # === 결제 내역 추적: 불법 재료를 많이 썼을수록 시간이 지나며 게이지가 샌다 ===
        self.inspection_gauge = min(
            INSPECTION_MAX,
            self.inspection_gauge + self.illegal_used * SUSPICION_LEAK * dt)

        # === 한울 검사 시스템: 주기/게이지로 등장, 검사 중엔 제한 시간이 흐른다 ===
        self.hanul_timer += dt
        if not self.hanul_active:
            if self.hanul_timer >= HANUL_INTERVAL or self.inspection_gauge >= HANUL_TRIGGER_GAUGE:
                self.hanul_active = True
                self.hanul_timer = 0.0
                self.hanul_time_left = HANUL_WINDOW
                self.repel_message = "한울이가 검사하러 왔다!"
        else:
            self.inspection_gauge = min(
                INSPECTION_MAX, self.inspection_gauge + HANUL_RISE_RATE * dt)
            self.hanul_time_left = max(0.0, self.hanul_time_left - dt)
            # 대처가 느리면 검증이 끝나 적발된다.
            if self.hanul_time_left <= 0:
                self.trigger_busted("느린 대처로 검증이 끝나버렸다")
                return

        # === 시간 종료 → 월세 정산 ===
        if self.time_left <= 0:
            self.time_left = 0.0
            self.phase = PHASE_GAME_OVER
            self.ending = "clear" if self.gold >= self.rent_goal else "rent_fail"

    @property
    def hanul_stage(self):
        """한울 검사 단계: '의심' → '검증' (UI 팝업용)."""
        if not self.hanul_active:
            return ""
        elapsed = HANUL_WINDOW - self.hanul_time_left
        return "검증" if elapsed >= HANUL_VERIFY_AT else "의심"

    @property
    def repel_recipe_names(self):
        """현재 필요한 퇴치 포션 재료 이름 목록 (UI 안내용)."""
        combo = REPEL_RECIPES.get(self.hanul_level, [[]])[0]
        return [get_ingredient(i)["name"] for i in combo if get_ingredient(i)]

    def next_customer(self):
        """스택에서 손님을 꺼내고 다음으로 이동. 빈 스택이면 정산."""
        if self.phase != PHASE_RESULT:
            return False
        self.customer_stack.pop()
        self._served += 1
        self._reset_brewing()
        self.last_result = None
        if self.customer_stack.is_empty():
            self.day_success = self.gold_today >= self.goal
            self.phase = PHASE_DAY_END
        else:
            self.phase = PHASE_ORDER
        return True

    def advance_day(self):
        """정산 후 진행: 성공이면 다음 날, 실패면 같은 날 재도전.

        마지막 날(FINAL_DAY)까지 성공하면 게임 클리어(성공 화면)로 끝낸다.
        """
        if self.phase != PHASE_DAY_END:
            return False
        if self.day_success:
            if self.day >= FINAL_DAY:
                self.phase = PHASE_GAME_OVER
                self.ending = "win"
                return True
            self.day += 1
        self.start_day()
        return True
