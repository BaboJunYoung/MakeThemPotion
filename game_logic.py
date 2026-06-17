"""Potion Workshop - 순수 게임 로직 (pygame 의존성 없음).

이 모듈은 렌더링/입력과 완전히 분리되어 있어 test.py 에서 독립적으로,
빠르고 안전하게 디버깅할 수 있다. main.py 는 GameState 를 호출하기만 한다.
"""

import random


# ---------------------------------------------------------------------------
# 데이터
# ---------------------------------------------------------------------------

INGREDIENTS = [
    {"id": "red_mushroom", "name": "붉은 버섯", "color": (217, 74, 74)},
    {"id": "blue_dew", "name": "푸른 이슬", "color": (74, 144, 217)},
    {"id": "yellow_petal", "name": "노란 꽃잎", "color": (242, 201, 76)},
    {"id": "black_root", "name": "검은 뿌리", "color": (58, 47, 69)},
    {"id": "star_dust", "name": "별가루", "color": (248, 233, 161)},
]

RECIPES = [
    {"potion_id": "healing", "name": "회복 포션",
     "ingredients": ["red_mushroom", "yellow_petal"], "color": (232, 77, 91)},
    {"potion_id": "sleep", "name": "수면 포션",
     "ingredients": ["blue_dew", "black_root"], "color": (53, 79, 140)},
    {"potion_id": "luck", "name": "행운 포션",
     "ingredients": ["yellow_petal", "star_dust"], "color": (242, 201, 76)},
    {"potion_id": "strength", "name": "힘 포션",
     "ingredients": ["red_mushroom", "star_dust"], "color": (242, 153, 74)},
]

FAILED_POTION = {
    "potion_id": "failed",
    "name": "수상한 포션",
    "ingredients": [],
    "color": (123, 114, 128),
}

CUSTOMERS = [
    {"id": "novice_adventurer", "name": "초보 모험가", "orders": ["healing", "strength"]},
    {"id": "sleepy_student", "name": "졸린 마법 학생", "orders": ["sleep"]},
    {"id": "unlucky_merchant", "name": "운 없는 상인", "orders": ["luck"]},
    {"id": "timid_knight", "name": "겁 많은 기사", "orders": ["strength", "luck"]},
    {"id": "tired_miner", "name": "지친 광부", "orders": ["strength", "healing"]},
    {"id": "suspicious_visitor", "name": "수상한 손님", "orders": ["sleep", "luck"]},
]

# 포션별 주문 대사
ORDER_LINES = {
    "healing": [
        "어제 던전에서 좀 구른 것 같아... 온몸이 욱신거려요.",
        "상처가 빨리 낫는 약이 있을까요?",
        "모험은 좋았는데, 돌아오는 길에 계단에서 굴렀어요.",
        "오늘 안에 다시 일어나야 해요. 몸을 회복시켜 주세요.",
    ],
    "sleep": [
        "요즘 잠을 통 못 자겠어요. 눈만 감으면 마법 시험 생각이 나요.",
        "옆집 마법사가 밤마다 폭발 실험을 해서 한숨도 못 잤어요.",
        "아주 깊고 조용한 잠이 필요해요.",
        "침대에 누워도 정신이 너무 또렷해요. 좀 잠들고 싶어요.",
    ],
    "luck": [
        "오늘 중요한 주사위 승부가 있어요. 운이 조금 필요합니다.",
        "고백하러 가는데... 성공 확률을 살짝 올리고 싶어요.",
        "요즘 장사가 너무 안 풀려요. 좋은 일이 생기는 약 없나요?",
        "시험 문제를 찍어야 할 것 같은데, 믿을 건 운뿐이에요.",
    ],
    "strength": [
        "오늘 광산에서 큰 바위를 치워야 해요.",
        "무거운 갑옷을 입고 하루 종일 버텨야 합니다.",
        "팔에 힘이 좀 붙는 약이 있나요?",
        "짐을 산처럼 옮겨야 해요. 힘이 필요합니다.",
    ],
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

# 하루 진행 설정: 손님 수, 등장 포션, 목표 골드
DAY_CONFIG = {
    1: {"customers": 3, "potions": ["healing", "strength"], "goal": 20},
    2: {"customers": 4, "potions": ["healing", "strength", "sleep"], "goal": 30},
    3: {"customers": 5, "potions": ["healing", "strength", "sleep", "luck"], "goal": 40},
}
# Day 4+ 공통 설정 (전체 랜덤)
DAY_DEFAULT = {"customers": 5, "potions": ["healing", "strength", "sleep", "luck"], "goal": 40}

REWARD_CORRECT = 10
REWARD_WRONG = 2

MAX_INGREDIENTS = 2

# 페이즈 상수
PHASE_ORDER = "order"        # 손님 주문 표시 / 재료 선택 대기
PHASE_BREWING = "brewing"    # 재료 선택 중
PHASE_CRAFTED = "crafted"    # 포션 완성, 제출 대기
PHASE_RESULT = "result"      # 제출 결과 표시
PHASE_DAY_END = "day_end"    # 하루 정산


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
    """재료 2개 조합으로 포션을 판정한다. 순서 무관. 매칭 실패 시 수상한 포션."""
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
# 게임 상태 (전체 흐름 관리, 렌더링 없음)
# ---------------------------------------------------------------------------

class GameState:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.day = 1
        self.gold = 0          # 누적 총 골드 (상단 표시)
        self.start_day()

    # --- 하루 시작 ---------------------------------------------------------
    def start_day(self):
        self.customers_today = generate_day_customers(self.day, self.rng)
        self.current_index = 0
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
        return len(self.customers_today)

    @property
    def current_customer(self):
        if 0 <= self.current_index < len(self.customers_today):
            return self.customers_today[self.current_index]
        return None

    def can_craft(self):
        return self.phase in (PHASE_ORDER, PHASE_BREWING) and len(self.selected) == MAX_INGREDIENTS

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

    def craft(self):
        """선택한 재료 2개로 포션 제작."""
        if not self.can_craft():
            return False
        self.crafted_potion = get_potion_by_ingredients(self.selected)
        self.phase = PHASE_CRAFTED
        return True

    def submit(self):
        """완성 포션을 현재 손님에게 제출하고 보상 처리."""
        if not self.can_submit():
            return False
        target = self.current_customer["target_potion"]
        correct, gold = evaluate(self.crafted_potion["potion_id"], target)
        self.gold += gold
        self.gold_today += gold
        reactions = CORRECT_REACTIONS if correct else WRONG_REACTIONS
        self.last_result = {
            "correct": correct,
            "gold": gold,
            "reaction": self.rng.choice(reactions),
            "potion": self.crafted_potion,
        }
        self.phase = PHASE_RESULT
        return True

    def next_customer(self):
        """다음 손님으로 이동. 마지막이면 정산으로."""
        if self.phase != PHASE_RESULT:
            return False
        self.current_index += 1
        self._reset_brewing()
        self.last_result = None
        if self.current_index >= self.total_customers:
            self.day_success = self.gold_today >= self.goal
            self.phase = PHASE_DAY_END
        else:
            self.phase = PHASE_ORDER
        return True

    def advance_day(self):
        """정산 후 진행: 성공이면 다음 날, 실패면 같은 날 재도전."""
        if self.phase != PHASE_DAY_END:
            return False
        if self.day_success:
            self.day += 1
        self.start_day()
        return True
