"""Potion Workshop - pygame UI.

게임 로직은 모두 game_logic.GameState 가 담당하고, 이 파일은 렌더링과
입력만 처리한다. 로직 검증은 test.py 에서 독립적으로 수행한다.

    python main.py
"""

import os
import sys

import pygame

import dialogue_engine as de
import game_logic as gl


# --- 화면/색상 설정 --------------------------------------------------------
WIDTH, HEIGHT = 960, 680
FPS = 60

BG = (43, 34, 28)            # 따뜻한 나무색 배경
PANEL = (60, 48, 40)
PANEL_LIGHT = (78, 63, 52)
ACCENT = (212, 175, 99)      # 약한 금색
TEXT = (240, 232, 218)
TEXT_DIM = (180, 168, 150)
CAULDRON = (38, 38, 44)
CAULDRON_RIM = (70, 70, 82)
GREEN = (120, 200, 120)
RED = (220, 110, 110)
SLOT_EMPTY = (52, 42, 35)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATHS = [
    os.path.join(BASE_DIR, "NotoSansKR-VF.ttf"),
    "/mnt/c/Windows/Fonts/malgun.ttf",
    "/mnt/c/Windows/Fonts/NotoSansKR-VF.ttf",
]
FONT_PATH = next((path for path in FONT_PATHS if os.path.exists(path)), None)


# 일반 손님 이름 (customer1/2 만 사용. customer3 은 한울이 전용이라 제외)
CUSTOMER_CHAR_NAMES = ["패션의 남자", "일하는 광부"]
HANUL_NAME = "한울이"

STREET_LINES = [
    ("주인공", "하아… 오늘도 평범한 하루네."),
    ("주인공", "과제는 많고, 시간은 없고…"),
    ("주인공", "이대로 어디 다른 세계라도 가버렸으면 좋겠다."),
    ("주인공", "...어?"),
    ("주인공", "잠깐, 여긴 인도인ㄷ—"),
    ("효과음", "끼이이익!"),
]

WHITEOUT_LINES = [
    ("주인공", "..."),
    ("주인공", "몸이… 안 움직여."),
    ("주인공", "여긴… 어디지?"),
]

FIRST_MEETING_STORE_LINES = [
    ("루미엘", "괜찮으세요?", "surprised"),
    ("주인공", "...", None),
    ("주인공", "...무척 귀엽잖아?", None),
    ("루미엘", "네?", "surprised"),
    ("주인공", "아, 아니요. 아무 말도 안 했습니다.", None),
    ("루미엘", "다행이에요. 길가에 쓰러져 계셔서 깜짝 놀랐답니다.", "smile"),
    ("주인공", "길가요?", None),
    ("루미엘", "네. 가게 앞에서요.", "normal"),
    ("주인공", "제가… 여기까지 어떻게 온 거죠?", None),
    ("루미엘", "그건 저도 잘 모르겠어요.", "normal"),
    ("루미엘", "하지만 이곳은 루미엘의 포션 가게랍니다.", "glad"),
    ("주인공", "포션 가게…", None),
]

# 첫 만남 CG(Lumiel_first_meeting) 위에서 보여줄 앞부분 줄 수.
# "괜찮으세요? / ... / 무척 귀엽잖아? / 네?" 까지 CG, 그 다음 줄부터 가게 내부로 전환.
FIRST_MEETING_CG_COUNT = 4

STORE_INTRO_LINES = [
    ("루미엘", "갈 곳이 없으시다면, 잠시 여기서 지내셔도 괜찮아요.", "smile"),
    ("주인공", "정말요?", None),
    ("루미엘", "대신…", "smile"),
    ("주인공", "대신?", None),
    ("루미엘", "그동안 가게 일을 조금만 도와주실 수 있을까요?", "smile"),
    ("주인공", "가게 일이라면… 포션 만드는 거요?", None),
    ("루미엘", "맞아요.", "glad"),
    ("루미엘", "저희 가게가 이제 막 차려져서 아직은 무명이라…", "normal"),
    ("루미엘", "손님이 많지는 않거든요.", "normal"),
    ("주인공", "그럼 그렇게 어렵진 않겠네요.", None),
    ("루미엘", "네. 단골 손님도 딱 세 명뿐이에요.", "glad"),
    ("주인공", "세 명이면 괜찮겠네요.", None),
    ("루미엘", "그런데…", "upset"),
    ("주인공", "그런데?", None),
    ("루미엘", "그 세 분이 조금 까다로워요.", "upset"),
    ("주인공", "조금이면 괜찮죠.", None),
    ("루미엘", "한 분은 렌몬 시럽이 안 들어가면 포션으로 인정하지 않고…", "upset"),
    ("루미엘", "한 분은 장식 세트가 없으면 가게 돈을 가져가고…", "upset"),
    ("루미엘", "마지막 한 분은…", "upset"),
    ("루미엘", "가게를 폐업시키려고 해요…", "upset"),
    ("주인공", "어떤 썩을 놈이…!", None),
    ("주인공", "그놈이 대체 누구죠?!", None),
    ("루미엘", "그게…", "upset"),
    ("루미엘", "『한울』이라는 식품위생관리원이 있는데…", "upset"),
    ("주인공", "식품위생관리원?", None),
    ("루미엘", "저희 가게에 강아지 털이 한 가닥 나왔다고 해서…", "upset"),
    ("루미엘", "폐업시키려고 해요… 흐윽.", "upset"),
    ("주인공", "저런 나쁜…", None),
    ("루미엘", "그래서…", "normal"),
    ("루미엘", "한울이에게 『특별 포션』을 드리려고요.", "smile"),
    ("주인공", "...네?", None),
    ("주인공", "잠깐만요.", None),
    ("주인공", "지금 들고 계신 거… 수상한 버섯 아닌가요?", "mushroom"),
    ("루미엘", "아뇨ㅎ 걱정마세요.", "mushroom"),
    ("주인공", "방금 ‘아뇨’랑 ‘걱정마세요’ 사이에 설명이 없었는데요?", None),
    ("루미엘", "괜찮아요.", "smile"),
    ("루미엘", "특별 포션이니까요.", "smile"),
    ("주인공", "그 특별함이 어느 쪽 특별함이죠?", None),
    ("루미엘", "도와주실 거죠?", "playful"),
    ("주인공", "...", None),
    ("루미엘", "도와주신다면 상으로…", "playful"),
    ("루미엘", "『특별한 선물』을 드릴게요♡", "smile"),
    ("주인공", "...물론이죠!", None),
    ("주인공", "제가 뭘 하면 되죠?", None),
    ("루미엘", "간단해요.", "smile"),
    ("루미엘", "손님이 오면, 원하는 재료를 넣어서 포션을 만들어 주세요.", "normal"),
    ("루미엘", "렌몬을 찾는 손님에겐 렌몬 시럽.", "normal"),
    ("루미엘", "꾸미고 싶어 하는 손님에겐 장식 세트.", "normal"),
    ("루미엘", "그리고 한울이가 오면…", "normal"),
    ("주인공", "오면?", None),
    ("루미엘", "상황에 맞게 잘 넘기면 돼요.", "smile"),
    ("주인공", "방금 굉장히 중요한 부분을 흐리셨는데요.", None),
    ("루미엘", "자, 그럼 오늘부터 잘 부탁드릴게요.", "glad"),
    ("주인공", "저 미소에 차마 거부할 수 없었다…", None),
    ("주인공", "이세계 생활 첫날.", None),
    ("주인공", "나는 포션 가게 알바가 되었다.", None),
    ("시스템", "첫 영업을 시작합니다.", None),
]


def make_font(size, bold=False):
    """한글 표시를 위해 시스템 폰트를 시도하고 실패 시 기본 폰트로 대체."""
    if FONT_PATH:
        font = pygame.font.Font(FONT_PATH, size)
        font.set_bold(bold)
        return font
    return pygame.font.SysFont(
        "malgungothic,applegothic,notosanscjkkr,gulim,arial", size, bold=bold
    )


class Button:
    # 모든 버튼이 공유하는 배경 이미지(준비된 button.png). Game 에서 1회 설정.
    shared_image = None

    def __init__(self, rect, label, font, color=ACCENT, text_color=(235, 226, 210)):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font = font
        self.color = color
        self.text_color = text_color
        self.enabled = True
        self._cache = {}   # size -> scaled image

    def _image_for_rect(self):
        if Button.shared_image is None:
            return None
        key = self.rect.size
        if key not in self._cache:
            self._cache[key] = pygame.transform.smoothscale(Button.shared_image, key)
        return self._cache[key]

    def draw(self, surf, mouse_pos):
        hovered = self.enabled and self.rect.collidepoint(mouse_pos)
        img = self._image_for_rect()
        if img is not None:
            # 별도 박스 없이 준비된 버튼 이미지만 사용. 호버는 밝게, 비활성은 어둡게.
            shade = img.copy()
            if not self.enabled:
                shade.fill((120, 120, 120, 255), special_flags=pygame.BLEND_RGB_MULT)
            elif hovered:
                shade.fill((40, 40, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
            surf.blit(shade, self.rect)
        else:
            color = (90, 82, 74) if not self.enabled else (
                tuple(min(255, c + 25) for c in self.color) if hovered else self.color)
            pygame.draw.rect(surf, color, self.rect, border_radius=10)
            pygame.draw.rect(surf, (30, 24, 20), self.rect, 2, border_radius=10)

        tc = self.text_color if self.enabled else (150, 142, 132)
        txt = self.font.render(self.label, True, tc)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)


def wrap_text(text, font, max_width):
    """공백/문자 단위로 줄바꿈. 한글은 단어 경계가 없으므로 문자 단위도 처리."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if font.size(trial)[0] <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                # 단어 자체가 너무 길면 문자 단위로 자른다.
                if font.size(word)[0] <= max_width:
                    current = word
                else:
                    chunk = ""
                    for ch in word:
                        if font.size(chunk + ch)[0] <= max_width:
                            chunk += ch
                        else:
                            lines.append(chunk)
                            chunk = ch
                    current = chunk
        lines.append(current)
    return lines


def draw_text(surf, text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surf.blit(img, rect)
    return rect


def load_image(name):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        return None
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error:
        return None


def load_sound(name):
    """효과음 로드. 파일이 없거나 믹서가 없으면 None (없어도 게임은 동작)."""
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        return None
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None


def crop_to_content(image, threshold=8):
    """투명 여백을 잘라내 아트 본체만 남긴다 (늘림/배치 정확도용)."""
    if image is None:
        return None
    mask = pygame.mask.from_surface(image, threshold)
    rects = mask.get_bounding_rects()
    if not rects:
        return image
    bbox = rects[0].copy()
    for rect in rects[1:]:
        bbox.union_ip(rect)
    return image.subsurface(bbox).copy()


def scale_cover(image, size):
    src_w, src_h = image.get_size()
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    scaled = pygame.transform.smoothscale(
        image, (max(1, int(src_w * scale)), max(1, int(src_h * scale)))
    )
    rect = scaled.get_rect(center=(dst_w // 2, dst_h // 2))
    canvas = pygame.Surface(size, pygame.SRCALPHA)
    canvas.blit(scaled, rect)
    return canvas


def fit_square(image, size):
    """이미지를 비율 유지한 채 size×size 투명 캔버스 중앙에 맞춘다 (아이콘용)."""
    src_w, src_h = image.get_size()
    scale = min(size / src_w, size / src_h)
    scaled = pygame.transform.smoothscale(
        image, (max(1, int(src_w * scale)), max(1, int(src_h * scale)))
    )
    canvas = pygame.Surface((size, size), pygame.SRCALPHA)
    canvas.blit(scaled, scaled.get_rect(center=(size // 2, size // 2)))
    return canvas


def scale_contain(image, size):
    src_w, src_h = image.get_size()
    dst_w, dst_h = size
    scale = min(dst_w / src_w, dst_h / src_h)
    scaled = pygame.transform.smoothscale(
        image, (max(1, int(src_w * scale)), max(1, int(src_h * scale)))
    )
    rect = scaled.get_rect(center=(dst_w // 2, dst_h // 2))
    canvas = pygame.Surface(size)
    canvas.fill((0, 0, 0))
    canvas.blit(scaled, rect)
    return canvas


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Potion Workshop")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_xl = make_font(46, bold=True)
        self.font_lg = make_font(30, bold=True)
        self.font_md = make_font(23)
        self.font_sm = make_font(19)
        self.font_xs = make_font(16)

        self.state = gl.GameState()
        self.drag_ingredient = None   # 드래그 중인 재료 id (없으면 None)
        self.drag_pos = (0, 0)        # 드래그 아이콘 현재 위치
        # 효과음 + 1회 재생 상태 추적 (전환 감지용)
        self.sfx = {}
        self._hanul_was_active = False
        self._hanul_verify_played = False
        self._game_over_played = False
        self.scene = "boot"    # boot / title / title_fade / intro / play
        self.boot_time = 0.0
        self.boot_duration = 0.9   # 검은 화면 → 타이틀 페이드아웃 시간
        self.title_fade_time = 0.0
        self.title_fade_duration = 0.25
        self.dialogue = de.DialogueController(WIDTH, HEIGHT, font_path=FONT_PATH,
                                              name_size=21, body_size=23, next_size=16)
        self.dialogue.set_actor_rect("left", pygame.Rect(32, 92, 190, 345))
        self.dialogue.set_visual_style(char_rise=6, chars_per_second=23,
                                       reveal_window=5.0,
                                       name_anchor=(0.165, 0.22))
        self.dialogue_key = None
        self.intro_started = False
        self.intro_phase = "street"
        self.intro_phase_order = ["street", "first_meeting", "store"]
        self.intro_effect_key = None
        self.intro_phase_time = 0.0
        self.auto_line_timer = 0.0
        self.collision_started = False
        self.collision_sound_timer = 0.0
        self.collision_blackout_time = 0.0
        self.collision_blackout_duration = 0.16   # beep 후 즉시 깜빡 (빠른 암전)
        self.collision_dialogue_closed = False
        self.intro_dialogue = de.DialogueController(
            WIDTH, HEIGHT, font_path=FONT_PATH,
            name_size=24, body_size=31, next_size=18,
        )
        # 캐릭터는 화면 정중앙(가로) + 바닥에 밀착시켜 하단 잘림이 벽에 닿게 한다.
        self.intro_dialogue.set_actor_rect(
            "center", pygame.Rect(WIDTH // 2 - 300, 30, 600, HEIGHT - 30))
        self.intro_dialogue.set_visual_style(char_rise=7, chars_per_second=23,
                                             reveal_window=5.6)

        # 이미지 리소스
        self.title_img = load_image("start_scene.png")
        self.street_img = load_image("street.png")
        self.first_meeting_img = load_image("Lumiel_first_meeting.png")
        self.truck_scene_img = load_image("truck_scene.png")
        self.store_bg = load_image("store_interior.png") or load_image("intro_bg.png")
        # 대화 상자는 투명 여백을 잘라내 실제 아트 비율(약 3.1:1)을 살린다.
        self.text_box_img = crop_to_content(load_image("text_box.png"))
        emotions = ["normal", "smile", "glad", "playful", "surprised", "upset", "mushroom"]
        raw_lumiel = {e: load_image(f"Lumiel_{e}.png") for e in emotions}
        fallback_lumiel = raw_lumiel.get("normal") or load_image("Lumiel_first_meeting.png")
        # 캐릭터 입상은 투명 여백을 잘라 중앙/바닥 정렬이 정확해지도록 한다.
        self.lumiel_images = {
            key: crop_to_content(image or fallback_lumiel)
            for key, image in raw_lumiel.items()
        }
        # 일반 손님은 customer1/2 만 사용한다 (customer3 은 한울이 전용).
        self.customer_images = [
            crop_to_content(load_image("customer1.png")),
            crop_to_content(load_image("customer2.png")),
        ]
        self.customer_images = [image for image in self.customer_images if image is not None]
        # 한울이: 평소엔 customer3 모습, 적발되면 한울이한테적발.png 로 변한다.
        self.hanul_image = crop_to_content(load_image("customer3.png"))
        self.caught_image = crop_to_content(load_image("한울이한테적발.png")) or self.hanul_image
        self.playful_cg = load_image("Lumiel_playful.png")
        # 가마솥 이미지 (비율 유지, 너비 220px 기준 스케일)
        self.cauldron_img = crop_to_content(load_image("cauldron.png"))
        if self.cauldron_img:
            _cw = 220
            _ch = int(_cw * self.cauldron_img.get_height() / self.cauldron_img.get_width())
            self.cauldron_img = pygame.transform.smoothscale(self.cauldron_img, (_cw, _ch))
        # 가게 내부 배경 (플레이 화면)
        self.shop_bg = load_image("가게내부.png") or self.store_bg
        if self.shop_bg:
            self.shop_bg = scale_cover(self.shop_bg, (WIDTH, HEIGHT))
        # 재료 아이콘 이미지 (id -> 잘라낸 원본). 표시 시 정사각형에 맞춰 캐싱한다.
        self.ingredient_images = {
            ing["id"]: crop_to_content(load_image(ing["image"]))
            for ing in gl.INGREDIENTS
        }
        self._icon_cache = {}
        # 포션 이미지: 준비된 8종을 15개 레시피에 순환 배정한다.
        potion_files = ["potion1.png", "potion2.png", "potion3.png", "potion4.png",
                        "red_potion.png", "green_potion.png", "blue_potion.png",
                        "pink_potion.png"]
        self.potion_images = {}
        for _i, _rec in enumerate(gl.RECIPES):
            _img = crop_to_content(load_image(potion_files[_i % len(potion_files)]))
            if _img:
                self.potion_images[_rec["potion_id"]] = _img
        self.lumiel_talk_sound = None
        self.beep_sound = None
        self.street_ambience_sound = None
        self.street_ambience_channel = None
        if self.title_img:
            self.title_img = scale_contain(self.title_img, (WIDTH, HEIGHT))
        if self.street_img:
            self.street_img = scale_cover(self.street_img, (WIDTH, HEIGHT))
        if self.first_meeting_img:
            self.first_meeting_img = scale_cover(self.first_meeting_img, (WIDTH, HEIGHT))
        if self.truck_scene_img:
            self.truck_scene_img = scale_cover(self.truck_scene_img, (WIDTH, HEIGHT))
        if self.store_bg:
            self.store_bg = scale_cover(self.store_bg, (WIDTH, HEIGHT))
        if self.playful_cg:
            self.playful_cg = scale_contain(self.playful_cg, (WIDTH, HEIGHT))

        # 준비된 버튼 이미지(button.png)를 모든 버튼이 공유한다.
        Button.shared_image = crop_to_content(load_image("button.png"))

        self._configure_dialogue_boxes()
        self._build_buttons()
        self.start_music()
        # 로딩이 끝난 뒤 클록을 리셋해 첫 프레임 dt가 수 초로 튀지 않게 한다.
        self.clock.tick()

    def _configure_dialogue_boxes(self):
        """대화 상자 이미지를 비율을 보존해 배치한다 (찌그러짐 방지)."""
        if not self.text_box_img:
            return
        ar = self.text_box_img.get_width() / self.text_box_img.get_height()
        self.intro_dialogue.set_box_image(self.text_box_img)
        self.dialogue.set_box_image(self.text_box_img)
        # 인트로: 하단 와이드 박스
        iw = WIDTH - 64
        ih = int(iw / ar)
        self.intro_dialogue.set_box_rect(
            pygame.Rect((WIDTH - iw) // 2, HEIGHT - ih - 16, iw, ih))
        # 플레이: 캐릭터(x≈14~214) 오른쪽에 배치해 겹침 방지
        pw = 580
        ph = int(pw / ar)
        self.dialogue.set_box_rect(pygame.Rect(240, 58, pw, ph))

    # --- 버튼 레이아웃 -----------------------------------------------------
    def _build_buttons(self):
        # 재료 버튼 10개 (하단 5열 × 2행 배치)
        self.ingredient_buttons = []
        cols, bw, bh, gx, gy = 5, 156, 64, 12, 10
        total = cols * bw + (cols - 1) * gx
        start_x = (WIDTH - total) // 2
        start_y = 430
        for i, ing in enumerate(gl.INGREDIENTS):
            row, col = divmod(i, cols)
            rect = pygame.Rect(start_x + col * (bw + gx),
                               start_y + row * (bh + gy), bw, bh)
            self.ingredient_buttons.append((ing, rect))

        # 액션 버튼 2개 (제작/제출, 중앙 정렬). 초기화 버튼은 없앰 — 재료를 다시 누르면 취소.
        aw, ag, ay = 240, 28, 578
        ax = (WIDTH - (aw * 2 + ag)) // 2
        self.btn_craft = Button((ax, ay, aw, 46), "제작하기", self.font_md)
        self.btn_submit = Button((ax + aw + ag, ay, aw, 46), "제출하기", self.font_md,
                                 color=GREEN, text_color=(20, 40, 20))
        self.btn_next = Button((WIDTH // 2 - 120, 462, 240, 54), "다음 손님", self.font_md)
        self.btn_advance = Button((WIDTH // 2 - 120, 462, 240, 54), "계속", self.font_md)
        self.btn_restart = Button((WIDTH // 2 - 120, 470, 240, 54), "다시 시작", self.font_md)
        self.btn_start = Button((WIDTH // 2 - 130, HEIGHT - 130, 260, 60),
                                "시작", self.font_md)

    def start_music(self):
        mixer_ready = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            mixer_ready = True
        except pygame.error:
            mixer_ready = False

        if mixer_ready:
            # 게임 효과음 로드 (없어도 무시). 발표용 피드백: 주문/정답/선택/클릭/등장/적발 등
            for name in ("message", "correct", "wrong", "select",
                         "click", "appearance", "inform", "caught"):
                self.sfx[name] = load_sound(f"{name}.mp3")
            talk_path = os.path.join(BASE_DIR, "Lumiel_talk.mp3")
            if os.path.exists(talk_path):
                try:
                    self.lumiel_talk_sound = pygame.mixer.Sound(talk_path)
                    self.intro_dialogue.set_type_sound(
                        self.lumiel_talk_sound,
                        interval=3,
                        volume=0.38,
                    )
                    self.dialogue.set_type_sound(
                        self.lumiel_talk_sound,
                        interval=3,
                        volume=0.38,
                    )
                except pygame.error:
                    self.lumiel_talk_sound = None
            beep_path = os.path.join(BASE_DIR, "beep.mp3")
            if os.path.exists(beep_path):
                try:
                    self.beep_sound = pygame.mixer.Sound(beep_path)
                    self.beep_sound.set_volume(0.8)
                except pygame.error:
                    self.beep_sound = None
            ambience_path = os.path.join(BASE_DIR, "street_ambience.mp3")
            if os.path.exists(ambience_path):
                try:
                    self.street_ambience_sound = pygame.mixer.Sound(ambience_path)
                    self.street_ambience_sound.set_volume(0.55)
                except pygame.error:
                    self.street_ambience_sound = None

        music_path = os.path.join(BASE_DIR, "Potion_Shop.mp3")
        if not os.path.exists(music_path):
            return
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.45)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def play_sfx(self, name):
        """효과음 1회 재생 (없으면 조용히 무시)."""
        snd = self.sfx.get(name)
        if snd:
            try:
                snd.play()
            except pygame.error:
                pass

    def handle_state_sounds(self):
        """게임 상태 전환을 감지해 알맞은 효과음을 1회씩 재생한다."""
        st = self.state
        # 한울 등장 → appearance 1회
        if st.hanul_active and not self._hanul_was_active:
            self.play_sfx("appearance")
            self._hanul_verify_played = False
        # 의심 → 검증 단계 진입 → inform 1회
        if st.hanul_active and st.hanul_stage == "검증" and not self._hanul_verify_played:
            self.play_sfx("inform")
            self._hanul_verify_played = True
        self._hanul_was_active = st.hanul_active
        # 게임오버 → 배경음 정지 후 caught 브금 1회
        if st.phase == gl.PHASE_GAME_OVER:
            if not self._game_over_played:
                try:
                    pygame.mixer.music.stop()
                except pygame.error:
                    pass
                # 성공 엔딩은 밝은 소리, 실패/적발은 caught 브금
                self.play_sfx("correct" if st.ending in ("win", "clear") else "caught")
                self._game_over_played = True
        else:
            self._game_over_played = False

    # --- 메인 루프 ---------------------------------------------------------
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # 인트로 스킵: Ctrl + Enter
                if (event.type == pygame.KEYDOWN
                        and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
                        and (event.mod & pygame.KMOD_CTRL)
                        and self.scene in ("boot", "title", "title_fade", "intro")):
                    self.skip_intro()
                    continue
                if (self.scene == "intro" and not self.is_intro_auto()
                        and self.intro_dialogue.handle_event(event)):
                    continue
                if self.scene == "play" and self.dialogue.handle_event(event):
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_down(event.pos)
                elif event.type == pygame.MOUSEMOTION and self.drag_ingredient:
                    self.drag_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.handle_mouse_up(event.pos)

            if self.scene == "intro":
                self.intro_phase_time += dt
                self.start_intro_if_needed()
                if not self.is_intro_phase_fading():
                    self.intro_dialogue.update(dt)
                    self.play_intro_line_effect()
                    self.update_intro_auto(dt)
                if self.intro_dialogue.finished and not self.waiting_for_collision_blackout():
                    next_phase = self.next_intro_phase()
                    if next_phase:
                        self.intro_phase = next_phase
                        self.intro_started = False
                        self.intro_effect_key = None
                        self.intro_phase_time = 0.0
                        self.auto_line_timer = 0.0
                        self.collision_started = False
                        self.collision_sound_timer = 0.0
                        self.collision_blackout_time = 0.0
                        self.collision_dialogue_closed = False
                        self.stop_street_ambience()
                    else:
                        self.scene = "play"
                        self.dialogue_key = None
            elif self.scene == "play":
                self.state.tick(dt)   # 제한 시간/검사 게이지/한울 갱신
                self.handle_state_sounds()
                self.sync_dialogue()
                self.dialogue.update(dt)
            elif self.scene == "title_fade":
                self.title_fade_time += dt
                if self.title_fade_time >= self.title_fade_duration:
                    self.begin_intro()
            elif self.scene == "boot":
                self.boot_time += dt
                if self.boot_time >= self.boot_duration:
                    self.scene = "title"

            if self.scene in ("title", "boot"):
                self.draw_title(mouse_pos)
                if self.scene == "boot":
                    # 완전 검은 화면에서 시작해 boot_duration 동안 페이드아웃
                    fade = 1.0 - de.ease_in_out_cubic(
                        min(1.0, self.boot_time / self.boot_duration))
                    if fade > 0:
                        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, int(255 * fade)))
                        self.screen.blit(overlay, (0, 0))
            elif self.scene == "title_fade":
                self.draw_title_fade(mouse_pos)
            elif self.scene == "intro":
                self.draw_intro()
            else:
                self.draw_play(mouse_pos)

            pygame.display.flip()

    # --- 입력 처리 ---------------------------------------------------------
    def cauldron_drop_rect(self):
        """재료를 드롭하면 가마솥에 들어가는 영역."""
        return pygame.Rect(WIDTH // 2 - 160, 230, 320, 235)

    def handle_mouse_down(self, pos):
        if self.scene in ("boot", "title_fade"):
            return
        if self.scene == "title":
            if self.btn_start.clicked(pos):
                self.play_sfx("click")
                self.scene = "title_fade"
                self.title_fade_time = 0.0
            return

        st = self.state
        phase = st.phase

        if phase in (gl.PHASE_ORDER, gl.PHASE_BREWING, gl.PHASE_CRAFTED):
            # 재료 버튼: 이미 선택된 재료면 취소, 아니면 드래그 시작
            for ing, rect in self.ingredient_buttons:
                if rect.collidepoint(pos):
                    if ing["id"] in st.selected:
                        st.remove_ingredient(ing["id"])
                        self.play_sfx("select")
                    elif phase in (gl.PHASE_ORDER, gl.PHASE_BREWING) \
                            and len(st.selected) < gl.MAX_INGREDIENTS:
                        self.drag_ingredient = ing["id"]
                        self.drag_pos = pos
                    return
            self.btn_craft.enabled = st.can_craft()
            if self.btn_craft.enabled and self.btn_craft.clicked(pos):
                self.play_sfx("click")
                st.craft()
                return
            self.btn_submit.enabled = st.can_submit()
            if self.btn_submit.enabled and self.btn_submit.clicked(pos):
                self.play_sfx("click")
                st.submit()
                # 주문 정답이면 correct, 틀리면 wrong 효과음
                if st.last_result:
                    self.play_sfx("correct" if st.last_result["correct"] else "wrong")
                return

        elif phase == gl.PHASE_RESULT:
            if self.btn_next.clicked(pos):
                self.play_sfx("click")
                st.next_customer()
                return

        elif phase == gl.PHASE_DAY_END:
            if self.btn_advance.clicked(pos):
                self.play_sfx("click")
                st.advance_day()
                self.dialogue_key = None
                return

        elif phase == gl.PHASE_GAME_OVER:
            # 엔딩 화면: 새 게임으로 리셋
            if self.btn_restart.clicked(pos):
                self.play_sfx("click")
                self.state = gl.GameState()
                self.drag_ingredient = None
                self.dialogue_key = None
                return

    def handle_mouse_up(self, pos):
        # 드래그 중인 재료를 가마솥 위에서 놓으면 추가, 다른 곳이면 취소
        if self.drag_ingredient is None:
            return
        iid = self.drag_ingredient
        self.drag_ingredient = None
        if self.cauldron_drop_rect().collidepoint(pos):
            if self.state.add_ingredient(iid):
                self.play_sfx("select")   # 포션 재료 선택마다

    def sync_dialogue(self):
        st = self.state
        if st.phase in (gl.PHASE_DAY_END, gl.PHASE_GAME_OVER):
            self.dialogue.clear()
            self.dialogue_key = None
            return

        # customer1/2 에 고정된 일반 손님 이름 사용 (customer3=한울이 제외)
        char_name = CUSTOMER_CHAR_NAMES[st.current_index % len(CUSTOMER_CHAR_NAMES)]

        if st.phase == gl.PHASE_RESULT and st.last_result:
            res = st.last_result
            key = ("result", st.day, st.current_index, res["reaction"])
            if key != self.dialogue_key:
                self.dialogue.set_script([de.DialogueLine(
                    speaker=char_name,
                    text=res["reaction"],
                    character_slot="left",
                    character_image=self.get_customer_image(st.current_index),
                    character_color=(120, 160, 115) if res["correct"] else (145, 95, 120),
                )], key=key)
                self.dialogue_key = key
            return

        cust = st.current_customer
        if not cust:
            self.dialogue.clear()
            self.dialogue_key = None
            return

        key = ("order", st.day, st.current_index, cust["order_line"])
        if key != self.dialogue_key:
            self.dialogue.set_script([de.DialogueLine(
                speaker=char_name,
                text=cust["order_line"],
                character_slot="left",
                character_image=self.get_customer_image(st.current_index),
                character_color=(110, 90, 140),
            )], key=key)
            self.dialogue_key = key
            self.play_sfx("message")   # 손님이 주문하면 1회 재생

    def get_customer_image(self, index):
        if not self.customer_images:
            return None
        return self.customer_images[index % len(self.customer_images)]

    def ingredient_icon(self, ingredient_id, size):
        """재료 아이콘을 size 정사각형으로 캐싱해 반환. 이미지 없으면 None."""
        image = self.ingredient_images.get(ingredient_id)
        if not image:
            return None
        key = (ingredient_id, size)
        if key not in self._icon_cache:
            self._icon_cache[key] = fit_square(image, size)
        return self._icon_cache[key]

    def next_intro_phase(self):
        try:
            index = self.intro_phase_order.index(self.intro_phase)
        except ValueError:
            return None
        if index + 1 >= len(self.intro_phase_order):
            return None
        return self.intro_phase_order[index + 1]

    def is_intro_auto(self):
        return self.intro_phase == "street" and self.intro_dialogue.index >= 3

    def intro_fade_duration(self):
        if self.intro_phase == "street":
            return 0.45
        if self.intro_phase == "first_meeting":
            return 0.75
        if self.intro_phase == "store":
            return 0.45   # 첫 만남 CG -> 가게 내부로 부드럽게 전환
        return 0.0

    def is_intro_phase_fading(self):
        return 0.0 <= self.intro_phase_time < self.intro_fade_duration()

    def begin_intro(self):
        self.scene = "intro"
        self.dialogue_key = None
        self.intro_phase = "street"
        self.intro_started = False
        self.intro_effect_key = None
        self.intro_phase_time = 0.0
        self.auto_line_timer = 0.0
        self.collision_started = False
        self.collision_sound_timer = 0.0
        self.collision_blackout_time = 0.0
        self.collision_dialogue_closed = False
        self.stop_street_ambience()

    def skip_intro(self):
        """` (backtick) 비밀 단축키: 인트로 전체를 즉시 스킵하고 플레이로 진입."""
        self.stop_street_ambience()
        self.intro_dialogue.clear()
        self.scene = "play"
        self.dialogue_key = None

    def waiting_for_collision_blackout(self):
        # 거리 장면이 끝나려면 암전이 완전히 덮인 뒤여야 한다 (street 노출 방지).
        return (
            self.intro_phase == "street"
            and self.collision_started
            and self.collision_blackout_time < self.collision_blackout_duration
        )

    def update_intro_auto(self, dt):
        # 트럭 효과음 / 거리 소음 타이머
        if self.collision_sound_timer > 0:
            self.collision_sound_timer = max(0.0, self.collision_sound_timer - dt)
            if self.collision_sound_timer <= 0:
                self.stop_street_ambience()

        # beep 가 끝나는 즉시 화면을 빠르게 암전시키고 대화를 닫는다.
        if self.collision_started and self.collision_sound_timer <= 0:
            if not self.collision_dialogue_closed:
                self.intro_dialogue.close()
                self.collision_dialogue_closed = True
            self.collision_blackout_time += dt

        if not self.is_intro_auto() or self.intro_dialogue.closing:
            return

        if not self.intro_dialogue.is_line_complete():
            self.intro_dialogue.complete_line()
            return

        # 마지막 줄(효과음)은 암전이 흐름을 이어가므로 자동으로 넘기지 않는다.
        if self.intro_dialogue.index >= len(self.intro_dialogue.lines) - 1:
            return

        line = self.intro_dialogue.current_line()
        self.auto_line_timer += dt
        delay = 0.32 if (line and line.speaker == "효과음") else 0.75
        if self.auto_line_timer >= delay:
            self.auto_line_timer = 0.0
            self.intro_dialogue.advance()

    def play_intro_line_effect(self):
        line = self.intro_dialogue.current_line()
        if not line:
            return
        key = (self.intro_phase, self.intro_dialogue.index)
        if key == self.intro_effect_key:
            return
        self.intro_effect_key = key
        if line.sound_effect:
            try:
                line.sound_effect.play()
            except pygame.error:
                pass
        # 효과음(트럭) 줄에 도달하면 충돌 연출을 시작한다. 소리가 없어도 진행.
        if self.intro_phase == "street" and line.speaker == "효과음":
            self.collision_started = True
            length = line.sound_effect.get_length() if line.sound_effect else 0.0
            self.collision_sound_timer = max(0.35, min(length, 1.2))
            self.play_street_ambience()

    def play_street_ambience(self):
        if not self.street_ambience_sound:
            return
        if self.street_ambience_channel and self.street_ambience_channel.get_busy():
            return
        try:
            self.street_ambience_channel = self.street_ambience_sound.play(loops=-1)
        except pygame.error:
            self.street_ambience_channel = None

    def stop_street_ambience(self):
        if not self.street_ambience_channel:
            return
        try:
            self.street_ambience_channel.fadeout(220)
        except pygame.error:
            pass
        self.street_ambience_channel = None

    def start_intro_if_needed(self):
        if self.intro_started:
            return
        if self.intro_phase == "street":
            lines = [
                de.DialogueLine(
                    speaker=speaker,
                    text=text,
                    character_slot=None,
                    background_image=self.truck_scene_img if index >= 3 else None,
                    sound_effect=self.beep_sound if speaker == "효과음" else None,
                )
                for index, (speaker, text) in enumerate(STREET_LINES)
            ]
            # street 씬 시작 즉시 ambient 재생 (beep 줄까지 기다리지 않는다).
            self.play_street_ambience()
        elif self.intro_phase == "first_meeting":
            # 첫 만남 CG 위에서 진행. "괜찮으세요? / ... / 무척 귀엽잖아? / 네?" 까지.
            lines = [
                de.DialogueLine(speaker=speaker, text=text, character_slot=None)
                for speaker, text in WHITEOUT_LINES
            ]
            for speaker, text, _emotion in FIRST_MEETING_STORE_LINES[:FIRST_MEETING_CG_COUNT]:
                lines.append(de.DialogueLine(
                    speaker=speaker, text=text, character_slot=None))
        else:
            # "네?" 이후부터는 가게 내부 배경 + 루미엘 입상으로 전환된다.
            lines = []
            for speaker, text, emotion in (
                    FIRST_MEETING_STORE_LINES[FIRST_MEETING_CG_COUNT:] + STORE_INTRO_LINES):
                if emotion is None and any(word in text for word in ("독버섯", "수상한 버섯", "버섯")):
                    emotion = "mushroom"
                lines.append(de.DialogueLine(
                    speaker=speaker, text=text,
                    character_slot="center" if (speaker == "루미엘" or emotion) else "keep",
                    character_image=self.lumiel_images[emotion] if emotion else None,
                    character_color=(160, 135, 190),
                ))
        self.intro_dialogue.set_script(
            lines,
            key=("intro", self.intro_phase),
            hide_on_finish=True,
        )
        self.intro_started = True

    # --- 그리기: 타이틀 ----------------------------------------------------
    def draw_title(self, mouse_pos):
        if self.title_img:
            self.screen.blit(self.title_img, (0, 0))
        else:
            self.screen.fill(BG)
        self.btn_start.draw(self.screen, mouse_pos)

    def draw_title_fade(self, mouse_pos):
        self.draw_title(mouse_pos)
        progress = de.ease_in_out_cubic(min(1.0, self.title_fade_time / self.title_fade_duration))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(255 * progress)))
        self.screen.blit(overlay, (0, 0))

    # --- 그리기: 인트로 ----------------------------------------------------
    def draw_intro(self):
        line = self.intro_dialogue.current_line()
        cg = line.background_image if line else None
        if cg:
            self.screen.blit(cg, (0, 0))
        elif self.intro_phase == "street":
            if self.street_img:
                self.screen.blit(self.street_img, (0, 0))
            else:
                self.screen.fill((30, 30, 34))
        elif self.intro_phase == "first_meeting" and self.first_meeting_img:
            self.screen.blit(self.first_meeting_img, (0, 0))
        elif self.store_bg:
            self.screen.blit(self.store_bg, (0, 0))
        else:
            self.screen.fill((24, 20, 28))

        fade_duration = self.intro_fade_duration()
        if fade_duration > 0:
            fade = 1.0 - de.ease_in_out_cubic(min(1.0, self.intro_phase_time / fade_duration))
            if fade > 0:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, int(255 * fade)))
                self.screen.blit(overlay, (0, 0))
                return

        if self.intro_phase == "street" and self.collision_started:
            blackout = de.ease_in_out_cubic(
                min(1.0, self.collision_blackout_time / self.collision_blackout_duration))
            if blackout > 0:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, int(255 * blackout)))
                self.screen.blit(overlay, (0, 0))
            if blackout >= 1.0:
                return

        self.intro_dialogue.draw(self.screen)

    # --- 그리기: 플레이 ----------------------------------------------------
    def draw_play(self, mouse_pos):
        # 가게 내부 배경 + 가독성을 위한 반투명 어둠막
        if self.shop_bg:
            self.screen.blit(self.shop_bg, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((20, 16, 12, 120))
            self.screen.blit(overlay, (0, 0))
        else:
            self.screen.fill(BG)
        self.draw_top_bar()
        self.draw_status()   # 검사 게이지 + 한울 등장 배너

        if self.state.phase == gl.PHASE_GAME_OVER:
            self.draw_game_over(mouse_pos)
            return
        if self.state.phase == gl.PHASE_DAY_END:
            self.draw_day_end(mouse_pos)
            return

        self.draw_customer()
        self.draw_cauldron()
        self.draw_order_indicator()
        self.draw_ingredients(mouse_pos)
        self.draw_action_buttons(mouse_pos)
        self.draw_drag()

        if self.state.phase == gl.PHASE_RESULT:
            self.draw_result_panel(mouse_pos)
        self.dialogue.draw(self.screen)

    def draw_drag(self):
        """드래그 중인 재료 아이콘을 커서를 따라 그린다."""
        if not self.drag_ingredient:
            return
        icon = self.ingredient_icon(self.drag_ingredient, 56)
        if icon:
            self.screen.blit(icon, icon.get_rect(center=self.drag_pos))
        else:
            pygame.draw.circle(self.screen, gl.get_ingredient(self.drag_ingredient)["color"],
                               self.drag_pos, 26)

    def draw_top_bar(self):
        st = self.state
        pygame.draw.rect(self.screen, PANEL, (0, 0, WIDTH, 50))
        draw_text(self.screen, f"Day {st.day}", self.font_lg, ACCENT, 20, 9)
        # === 월세 목표 시스템: 현재 돈 / 목표 월세 ===
        reached = st.gold >= st.rent_goal
        money_col = GREEN if reached else (242, 201, 76)
        draw_text(self.screen, f"{st.gold} / {st.rent_goal} G", self.font_lg, money_col,
                  WIDTH // 2, 25, center=True)
        draw_text(self.screen, "월세", self.font_xs, TEXT_DIM, WIDTH // 2, 2, center=True)
        # === 제한 시간 시스템: 남은 시간 ===
        secs = int(st.time_left)
        time_txt = f"남은 시간 {secs // 60}:{secs % 60:02d}"
        time_col = RED if secs <= 15 else TEXT
        draw_text(self.screen, time_txt, self.font_md, time_col,
                  WIDTH - 20 - self.font_md.size(time_txt)[0], 13)

    def draw_status(self):
        """한울 검사 게이지 바 + 한울 등장 배너."""
        st = self.state
        # === 한울 검사 게이지 (상단 바 아래 표시) ===
        bx, by, bw, bh = 20, 56, 260, 16
        ratio = st.inspection_gauge / gl.INSPECTION_MAX
        draw_text(self.screen, "검사 위험도", self.font_xs, TEXT_DIM, bx, by - 16)
        pygame.draw.rect(self.screen, (40, 34, 30), (bx, by, bw, bh), border_radius=8)
        if ratio > 0:
            col = RED if ratio >= 0.7 else (ACCENT if ratio >= 0.4 else GREEN)
            pygame.draw.rect(self.screen, col,
                             (bx, by, int(bw * min(1.0, ratio)), bh), border_radius=8)
        pygame.draw.rect(self.screen, (100, 88, 76), (bx, by, bw, bh), 1, border_radius=8)
        draw_text(self.screen, f"{int(st.inspection_gauge)}/100", self.font_xs, TEXT_DIM,
                  bx + bw + 10, by - 1)

        # === 한울 검사 시스템: 상단 팝업 (의심/검증 단계 + 제한 시간 + customer3 모습) ===
        if st.hanul_active and st.phase not in (gl.PHASE_GAME_OVER, gl.PHASE_DAY_END):
            banner = pygame.Rect(WIDTH // 2 - 270, 80, 540, 62)
            verifying = st.hanul_stage == "검증"
            pygame.draw.rect(self.screen, (110, 26, 32) if verifying else (90, 30, 36),
                             banner, border_radius=10)
            pygame.draw.rect(self.screen, RED, banner, 2, border_radius=10)
            # 한울이는 처음 등장할 땐 customer3 의 모습
            if self.hanul_image:
                portrait = fit_square(self.hanul_image, 52)
                self.screen.blit(portrait, (banner.x + 8, banner.y + 5))
            secs = int(st.hanul_time_left) + 1
            stage_txt = f"[{st.hanul_stage} 단계]  검증까지 {secs}초"
            draw_text(self.screen, f"한울이가 검사하러 왔다!  {stage_txt}",
                      self.font_sm, (255, 225, 225), banner.centerx + 24, banner.y + 16,
                      center=True)
            repel = " + ".join(st.repel_recipe_names)
            draw_text(self.screen, f"퇴치 포션: {repel} 제작!", self.font_xs,
                      (255, 205, 205), banner.centerx + 24, banner.y + 42, center=True)
            # 남은 시간 막대
            ratio = st.hanul_time_left / gl.HANUL_WINDOW
            pygame.draw.rect(self.screen, (60, 24, 26),
                             (banner.x + 64, banner.bottom - 9, banner.width - 80, 5),
                             border_radius=3)
            pygame.draw.rect(self.screen, (255, 120, 110),
                             (banner.x + 64, banner.bottom - 9,
                              int((banner.width - 80) * max(0.0, ratio)), 5), border_radius=3)

    def draw_customer(self):
        st = self.state
        cust = st.current_customer
        if not cust:
            return
        shadow = pygame.Surface((200, 22), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 55), shadow.get_rect())
        self.screen.blit(shadow, (14, HEIGHT - 28))

    def draw_cauldron(self):
        st = self.state
        cx, cy = WIDTH // 2, 318

        # 드래그 중이면 드롭 영역을 강조 표시한다.
        if self.drag_ingredient:
            drop = self.cauldron_drop_rect()
            hl = pygame.Surface(drop.size, pygame.SRCALPHA)
            pygame.draw.rect(hl, (212, 175, 99, 45), hl.get_rect(), border_radius=16)
            pygame.draw.rect(hl, (212, 175, 99, 170), hl.get_rect(), 3, border_radius=16)
            self.screen.blit(hl, drop)

        # 선택 재료 슬롯 (최대 3개, 가마솥 위쪽). 채워지면 재료 아이콘 표시.
        slot_w, slot_h, sgap = 84, 46, 12
        n = gl.MAX_INGREDIENTS
        sx = cx - (n * slot_w + (n - 1) * sgap) // 2
        for i in range(n):
            slot = pygame.Rect(sx + i * (slot_w + sgap), 248, slot_w, slot_h)
            filled = i < len(st.selected)
            pygame.draw.rect(self.screen, PANEL_LIGHT if filled else SLOT_EMPTY,
                             slot, border_radius=10)
            pygame.draw.rect(self.screen, CAULDRON_RIM, slot, 2, border_radius=10)
            if filled:
                iid = st.selected[i]
                icon = self.ingredient_icon(iid, slot_h - 8)
                if icon:
                    self.screen.blit(icon, icon.get_rect(center=slot.center))
                else:
                    pygame.draw.circle(self.screen, gl.get_ingredient(iid)["color"],
                                       slot.center, 16)

        # 가마솥 이미지 (없으면 폴백 도형)
        if self.cauldron_img:
            self.screen.blit(self.cauldron_img, self.cauldron_img.get_rect(center=(cx, cy)))
        else:
            pygame.draw.ellipse(self.screen, CAULDRON_RIM, (cx - 130, cy - 70, 260, 60))
            pygame.draw.rect(self.screen, CAULDRON, (cx - 120, cy - 50, 240, 110),
                             border_radius=20)
            pygame.draw.ellipse(self.screen, (24, 24, 30), (cx - 110, cy - 62, 220, 44))
            lc = None
            if st.crafted_potion:
                lc = st.crafted_potion["color"]
            elif st.selected:
                cols = [gl.get_ingredient(ii)["color"] for ii in st.selected]
                lc = tuple(sum(c[k] for c in cols) // len(cols) for k in range(3))
            if lc:
                pygame.draw.ellipse(self.screen, lc, (cx - 95, cy - 56, 190, 34))

        # 완성 포션: 이미지를 가마솥 위에 띄우고 이름 표시
        if st.crafted_potion:
            pid = st.crafted_potion["potion_id"]
            pimg = self.potion_images.get(pid)
            if pimg:
                scaled = pygame.transform.smoothscale(pimg, (76, 76))
                self.screen.blit(scaled, scaled.get_rect(center=(cx, cy - 16)))
            draw_text(self.screen, f"완성: {st.crafted_potion['name']}",
                      self.font_lg, st.crafted_potion["color"], cx, cy + 82, center=True)
        else:
            draw_text(self.screen, "재료를 가마솥으로 끌어다 넣으세요", self.font_sm,
                      TEXT_DIM, cx, cy + 82, center=True)
            draw_text(self.screen, "넣은 재료를 다시 누르면 취소", self.font_xs,
                      TEXT_DIM, cx, cy + 106, center=True)

    def draw_order_indicator(self):
        """우측 패널: 원하는 포션 + 그 아래 필요한 재료 아이콘을 표시."""
        st = self.state
        if st.phase not in (gl.PHASE_ORDER, gl.PHASE_BREWING, gl.PHASE_CRAFTED):
            return
        cust = st.current_customer
        if not cust:
            return
        recipe = gl.get_recipe(cust["target_potion"])
        if not recipe:
            return

        pw, ph = 188, 176
        px, py = WIDTH - pw - 14, 238
        cx = px + pw // 2
        panel = pygame.Rect(px, py, pw, ph)
        pygame.draw.rect(self.screen, PANEL, panel, border_radius=12)
        pygame.draw.rect(self.screen, ACCENT, panel, 2, border_radius=12)

        draw_text(self.screen, "손님 주문", self.font_xs, TEXT_DIM, cx, py + 16, center=True)

        pimg = self.potion_images.get(recipe["potion_id"])
        if pimg:
            big = pygame.transform.smoothscale(pimg, (64, 64))
            self.screen.blit(big, big.get_rect(center=(cx, py + 56)))
        else:
            pygame.draw.circle(self.screen, recipe["color"], (cx, py + 56), 30)
        draw_text(self.screen, recipe["name"], self.font_sm, TEXT, cx, py + 96, center=True)

        # 구분선 + 필요한 재료 아이콘 (주문 하단)
        pygame.draw.line(self.screen, (100, 88, 76),
                         (px + 16, py + 116), (px + pw - 16, py + 116))
        draw_text(self.screen, "필요한 재료", self.font_xs, TEXT_DIM, cx, py + 130, center=True)
        ings = recipe["ingredients"]
        isize, igap = 34, 8
        ix = cx - (len(ings) * isize + (len(ings) - 1) * igap) // 2
        for k, iid in enumerate(ings):
            rect = pygame.Rect(ix + k * (isize + igap), py + 142, isize, isize)
            icon = self.ingredient_icon(iid, isize)
            if icon:
                self.screen.blit(icon, rect)
            else:
                pygame.draw.circle(self.screen, gl.get_ingredient(iid)["color"],
                                   rect.center, isize // 2)

    def draw_ingredients(self, mouse_pos):
        st = self.state
        for ing, rect in self.ingredient_buttons:
            selected = ing["id"] in st.selected
            disabled = (selected or len(st.selected) >= gl.MAX_INGREDIENTS
                        or st.phase == gl.PHASE_CRAFTED)
            hovered = rect.collidepoint(mouse_pos) and not disabled
            bg = PANEL_LIGHT if not selected else (40, 60, 40)
            if hovered:
                bg = tuple(min(255, c + 18) for c in bg)
            pygame.draw.rect(self.screen, bg, rect, border_radius=12)
            # 불법 재료 리스크 시스템: 수상한 재료는 빨간 테두리로 구분
            if selected:
                border = GREEN
            elif ing["suspicious"]:
                border = RED
            else:
                border = ACCENT
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=12)
            # 재료 아이콘 (이미지, 없으면 색 원으로 폴백)
            icon = self.ingredient_icon(ing["id"], 38)
            if icon:
                self.screen.blit(icon, icon.get_rect(center=(rect.centerx, rect.y + 24)))
            else:
                pygame.draw.circle(self.screen, ing["color"], (rect.centerx, rect.y + 24), 18)
            draw_text(self.screen, ing["name"], self.font_xs,
                      TEXT_DIM if disabled and not selected else TEXT,
                      rect.centerx, rect.bottom - 13, center=True)
            # 수상한(불법) 재료 표식
            if ing["suspicious"]:
                tag = pygame.Rect(rect.right - 38, rect.y + 5, 33, 16)
                pygame.draw.rect(self.screen, (140, 40, 46), tag, border_radius=5)
                draw_text(self.screen, "수상", self.font_xs, (255, 220, 220),
                          tag.centerx, tag.centery, center=True)

    def draw_action_buttons(self, mouse_pos):
        st = self.state
        self.btn_craft.enabled = st.can_craft()
        self.btn_submit.enabled = st.can_submit()
        self.btn_craft.draw(self.screen, mouse_pos)
        self.btn_submit.draw(self.screen, mouse_pos)

    def draw_result_panel(self, mouse_pos):
        st = self.state
        res = st.last_result
        # 어둡게 덮기
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 8, 6, 180))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 280, 150, 560, 360)
        pygame.draw.rect(self.screen, PANEL, panel, border_radius=20)
        pygame.draw.rect(self.screen, ACCENT, panel, 3, border_radius=20)

        title = "정답!" if res["correct"] else "아쉬워요"
        color = GREEN if res["correct"] else RED
        draw_text(self.screen, title, self.font_xl, color, WIDTH // 2, panel.y + 50,
                  center=True)

        lines = wrap_text(res["reaction"], self.font_md, panel.width - 80)
        ty = panel.y + 110
        for line in lines:
            draw_text(self.screen, line, self.font_md, TEXT, WIDTH // 2, ty, center=True)
            ty += 34

        draw_text(self.screen, f"제출: {res['potion']['name']}", self.font_sm,
                  TEXT_DIM, WIDTH // 2, ty + 10, center=True)
        # 정답이면 +수입(금색), 틀리면 돈을 빼앗김(빨강)
        gold = res["gold"]
        money_txt = f"+{gold} Gold" if gold >= 0 else f"{gold} Gold"
        draw_text(self.screen, money_txt, self.font_lg,
                  (242, 201, 76) if gold >= 0 else RED, WIDTH // 2, ty + 50, center=True)

        last = st.current_index + 1 >= st.total_customers
        self.btn_next.label = "하루 정산" if last else "다음 손님"
        self.btn_next.draw(self.screen, mouse_pos)

    def draw_day_end(self, mouse_pos):
        st = self.state
        panel = pygame.Rect(WIDTH // 2 - 280, 130, 560, 400)
        pygame.draw.rect(self.screen, PANEL, panel, border_radius=20)
        pygame.draw.rect(self.screen, ACCENT, panel, 3, border_radius=20)

        draw_text(self.screen, f"Day {st.day} 종료", self.font_xl, ACCENT,
                  WIDTH // 2, panel.y + 55, center=True)
        draw_text(self.screen, f"오늘 번 골드: {st.gold_today} G", self.font_lg, TEXT,
                  WIDTH // 2, panel.y + 130, center=True)
        draw_text(self.screen, f"목표 골드: {st.goal} G", self.font_md, TEXT_DIM,
                  WIDTH // 2, panel.y + 175, center=True)

        if st.day_success:
            draw_text(self.screen, "목표 달성! 성공", self.font_lg, GREEN,
                      WIDTH // 2, panel.y + 235, center=True)
            self.btn_advance.label = "다음 날로"
        else:
            draw_text(self.screen, "목표 미달... 같은 날 재도전", self.font_lg, RED,
                      WIDTH // 2, panel.y + 235, center=True)
            self.btn_advance.label = "다시 도전"
        # 월세 진행 상황도 함께 보여준다.
        draw_text(self.screen, f"월세 {st.gold} / {st.rent_goal} G  ·  남은 시간 {int(st.time_left)}초",
                  self.font_sm, TEXT_DIM, WIDTH // 2, panel.y + 300, center=True)
        self.btn_advance.draw(self.screen, mouse_pos)

    def draw_game_over(self, mouse_pos):
        """월세 성공/실패/적발 엔딩 화면. 적발 시 '한울이한테적발' 모습으로 등장."""
        st = self.state
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 6, 6, 215))
        self.screen.blit(overlay, (0, 0))

        if st.ending == "win":
            title, color = "Day 3 클리어! 게임 성공", GREEN
            lines = ["사흘간의 영업을 모두 무사히 마쳤다!",
                     "루미엘의 포션 가게를 끝까지 지켜냈다."]
        elif st.ending == "clear":
            title, color = "가게를 지켰다!", GREEN
            lines = ["제한 시간 안에 월세를 모두 갚았다.",
                     "루미엘의 포션 가게는 오늘도 무사하다."]
        elif st.ending == "busted":
            title, color = "한울이한테 적발!", RED
            lines = [st.caught_reason or "불법 재료가 들통났다.",
                     "가게는 영업정지 처분을 받았다..."]
            # 적발 엔딩: 한울이가 '한울이한테적발' 모습으로 크게 등장
            if self.caught_image:
                big = fit_square(self.caught_image, 300)
                self.screen.blit(big, big.get_rect(center=(WIDTH // 2, 220)))
        else:  # rent_fail
            title, color = "가게가 망했다...", RED
            lines = ["시간이 다 됐지만 월세를 내지 못했다.",
                     f"모은 돈 {st.gold} G / 목표 {st.rent_goal} G"]

        # 적발 화면은 캐릭터를 보여주므로 패널을 아래쪽에 배치
        panel_y = 380 if st.ending == "busted" else 180
        panel = pygame.Rect(WIDTH // 2 - 300, panel_y, 600, 260)
        pygame.draw.rect(self.screen, PANEL, panel, border_radius=20)
        pygame.draw.rect(self.screen, color, panel, 3, border_radius=20)

        draw_text(self.screen, title, self.font_xl, color,
                  WIDTH // 2, panel.y + 44, center=True)
        ty = panel.y + 100
        for line in lines:
            draw_text(self.screen, line, self.font_md, TEXT, WIDTH // 2, ty, center=True)
            ty += 34
        draw_text(self.screen, f"최종 자금 {st.gold} G", self.font_sm, (242, 201, 76),
                  WIDTH // 2, panel.y + 178, center=True)
        self.btn_restart.rect.center = (WIDTH // 2, panel.y + 222)
        self.btn_restart.draw(self.screen, mouse_pos)


if __name__ == "__main__":
    Game().run()
