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


# customer1/2/3.png 에 고정된 캐릭터 이름 (이미지 인덱스 순서)
CUSTOMER_CHAR_NAMES = ["패션의 남자", "일하는 광부", "남자3"]

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
        self.customer_images = [
            crop_to_content(load_image("customer1.png")),
            crop_to_content(load_image("customer2.png")),
            crop_to_content(load_image("customer3.png")),
        ]
        self.customer_images = [image for image in self.customer_images if image is not None]
        self.playful_cg = load_image("Lumiel_playful.png")
        # 가마솥 이미지 (비율 유지, 너비 280px 기준 스케일)
        self.cauldron_img = crop_to_content(load_image("cauldron.png"))
        if self.cauldron_img:
            _cw = 280
            _ch = int(_cw * self.cauldron_img.get_height() / self.cauldron_img.get_width())
            self.cauldron_img = pygame.transform.smoothscale(self.cauldron_img, (_cw, _ch))
        # 포션 이미지 (RECIPES 순서: healing, sleep, luck, strength → potion1~4)
        self.potion_images = {}
        for _i, _rec in enumerate(gl.RECIPES, start=1):
            _img = crop_to_content(load_image(f"potion{_i}.png"))
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
        # 재료 버튼 5개 (하단 가로 배치 — 레시피 공간 확보를 위해 높이 축소)
        self.ingredient_buttons = []
        n = len(gl.INGREDIENTS)
        bw, bh, gap = 148, 76, 12
        total = n * bw + (n - 1) * gap
        start_x = (WIDTH - total) // 2
        y = 426
        for i, ing in enumerate(gl.INGREDIENTS):
            rect = pygame.Rect(start_x + i * (bw + gap), y, bw, bh)
            self.ingredient_buttons.append((ing, rect))

        # 액션 버튼 (레시피 띠를 위해 y=528로 올림)
        ay = 528
        self.btn_clear = Button((start_x, ay, 224, 50), "초기화", self.font_md,
                                color=(150, 110, 90), text_color=TEXT)
        self.btn_craft = Button((start_x + 244, ay, 224, 50), "제작하기", self.font_md)
        self.btn_submit = Button((start_x + 488, ay, 224, 50), "제출하기", self.font_md,
                                 color=GREEN, text_color=(20, 40, 20))
        self.btn_next = Button((WIDTH // 2 - 120, 462, 240, 54), "다음 손님", self.font_md)
        self.btn_advance = Button((WIDTH // 2 - 120, 462, 240, 54), "계속", self.font_md)
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
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_BACKQUOTE
                        and self.scene in ("boot", "title", "title_fade", "intro")):
                    self.skip_intro()
                    continue
                if (self.scene == "intro" and not self.is_intro_auto()
                        and self.intro_dialogue.handle_event(event)):
                    continue
                if self.scene == "play" and self.dialogue.handle_event(event):
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

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
    def handle_click(self, pos):
        if self.scene in ("boot", "title_fade"):
            return
        if self.scene == "title":
            if self.btn_start.clicked(pos):
                self.scene = "title_fade"
                self.title_fade_time = 0.0
            return

        st = self.state
        phase = st.phase

        if phase in (gl.PHASE_ORDER, gl.PHASE_BREWING, gl.PHASE_CRAFTED):
            # 재료 추가
            if phase in (gl.PHASE_ORDER, gl.PHASE_BREWING):
                for ing, rect in self.ingredient_buttons:
                    if rect.collidepoint(pos):
                        st.add_ingredient(ing["id"])
                        return
            if self.btn_clear.clicked(pos):
                st.clear_ingredients()
                return
            self.btn_craft.enabled = st.can_craft()
            if self.btn_craft.enabled and self.btn_craft.clicked(pos):
                st.craft()
                return
            self.btn_submit.enabled = st.can_submit()
            if self.btn_submit.enabled and self.btn_submit.clicked(pos):
                st.submit()
                return

        elif phase == gl.PHASE_RESULT:
            if self.btn_next.clicked(pos):
                st.next_customer()
                return

        elif phase == gl.PHASE_DAY_END:
            if self.btn_advance.clicked(pos):
                st.advance_day()
                self.dialogue_key = None
                return

    def sync_dialogue(self):
        st = self.state
        if st.phase == gl.PHASE_DAY_END:
            self.dialogue.clear()
            self.dialogue_key = None
            return

        # 이미지 파일 순서(customer1/2/3)에 고정된 캐릭터 이름 사용
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

    def get_customer_image(self, index):
        if not self.customer_images:
            return None
        return self.customer_images[index % len(self.customer_images)]

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
        self.screen.fill(BG)
        self.draw_top_bar()

        if self.state.phase == gl.PHASE_DAY_END:
            self.draw_day_end(mouse_pos)
            return

        self.draw_customer()
        self.draw_cauldron()
        self.draw_order_indicator()
        self.draw_ingredients(mouse_pos)
        self.draw_action_buttons(mouse_pos)
        self.draw_recipe_reference()

        if self.state.phase == gl.PHASE_RESULT:
            self.draw_result_panel(mouse_pos)
        self.dialogue.draw(self.screen)

    def draw_top_bar(self):
        st = self.state
        pygame.draw.rect(self.screen, PANEL, (0, 0, WIDTH, 50))
        draw_text(self.screen, f"Day {st.day}", self.font_lg, ACCENT, 20, 9)
        draw_text(self.screen, f"Gold {st.gold}", self.font_lg, (242, 201, 76),
                  WIDTH // 2, 25, center=True)
        progress = f"{min(st.current_index + 1, st.total_customers)} / {st.total_customers}"
        draw_text(self.screen, f"손님 {progress}", self.font_md, TEXT,
                  WIDTH - 20 - self.font_md.size(f"손님 {progress}")[0], 13)
        draw_text(self.screen, f"목표 {st.goal} G", self.font_xs, TEXT_DIM,
                  WIDTH - 200, 56)

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
        cx, cy = WIDTH // 2, 330

        # 선택 재료 슬롯 2개 (가마솥 위쪽)
        for i in range(gl.MAX_INGREDIENTS):
            slot = pygame.Rect(cx - 120 + i * 130, 250, 110, 46)
            filled = i < len(st.selected)
            ing_color = gl.get_ingredient(st.selected[i])["color"] if filled else SLOT_EMPTY
            pygame.draw.rect(self.screen, ing_color, slot, border_radius=10)
            pygame.draw.rect(self.screen, CAULDRON_RIM, slot, 2, border_radius=10)
            if filled:
                draw_text(self.screen, gl.get_ingredient(st.selected[i])["name"],
                          self.font_sm, (20, 18, 16), slot.centerx, slot.centery, center=True)

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
            draw_text(self.screen, "재료 2개를 넣고 제작하세요", self.font_sm,
                      TEXT_DIM, cx, cy + 82, center=True)

    def draw_recipe_reference(self):
        """하단: 4가지 레시피를 2열로 항상 표시."""
        ry = 586
        rh = 88
        panel = pygame.Rect(14, ry, WIDTH - 28, rh)
        pygame.draw.rect(self.screen, PANEL, panel, border_radius=8)
        pygame.draw.rect(self.screen, (100, 88, 76), panel, 1, border_radius=8)

        draw_text(self.screen, "레시피", self.font_xs, TEXT_DIM, 28, ry + 10)

        col_x = [90, 90 + (WIDTH - 104) // 2]
        rows = [gl.RECIPES[:2], gl.RECIPES[2:]]
        for row_i, row in enumerate(rows):
            for col_i, recipe in enumerate(row):
                x = col_x[col_i]
                y = ry + 10 + row_i * 38
                ings = [gl.get_ingredient(iid)["name"] for iid in recipe["ingredients"]]
                label = f"{recipe['name']}: {ings[0]} + {ings[1]}"
                # 포션 이름은 포션 색으로, 재료는 TEXT_DIM 으로 구분
                draw_text(self.screen, recipe["name"] + ": ", self.font_xs,
                          recipe["color"], x, y)
                name_w = self.font_xs.size(recipe["name"] + ": ")[0]
                draw_text(self.screen, f"{ings[0]} + {ings[1]}", self.font_xs,
                          TEXT_DIM, x + name_w, y)

    def draw_order_indicator(self):
        """우측 패널: 현재 손님이 원하는 포션을 이미지+이름으로 명확히 표시."""
        st = self.state
        if st.phase not in (gl.PHASE_ORDER, gl.PHASE_BREWING, gl.PHASE_CRAFTED):
            return
        cust = st.current_customer
        if not cust:
            return
        recipe = gl.get_recipe(cust["target_potion"])
        if not recipe:
            return

        pw, ph = 160, 170
        px, py = WIDTH - pw - 14, 258
        panel = pygame.Rect(px, py, pw, ph)
        pygame.draw.rect(self.screen, PANEL, panel, border_radius=12)
        pygame.draw.rect(self.screen, ACCENT, panel, 2, border_radius=12)

        draw_text(self.screen, "손님 주문", self.font_xs, TEXT_DIM,
                  panel.centerx, py + 16, center=True)

        pimg = self.potion_images.get(recipe["potion_id"])
        if pimg:
            big = pygame.transform.smoothscale(pimg, (84, 84))
            self.screen.blit(big, big.get_rect(center=(panel.centerx, py + 88)))
        else:
            pygame.draw.circle(self.screen, recipe["color"], (panel.centerx, py + 88), 38)

        draw_text(self.screen, recipe["name"], self.font_sm, TEXT,
                  panel.centerx, py + 148, center=True)

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
            border = GREEN if selected else ACCENT
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=12)
            # 재료 아이콘 (색 원)
            pygame.draw.circle(self.screen, ing["color"], (rect.centerx, rect.y + 32), 22)
            pygame.draw.circle(self.screen, (20, 18, 16), (rect.centerx, rect.y + 32), 22, 2)
            draw_text(self.screen, ing["name"], self.font_sm,
                      TEXT_DIM if disabled and not selected else TEXT,
                      rect.centerx, rect.bottom - 16, center=True)

    def draw_action_buttons(self, mouse_pos):
        st = self.state
        self.btn_craft.enabled = st.can_craft()
        self.btn_submit.enabled = st.can_submit()
        self.btn_clear.enabled = (st.phase in (gl.PHASE_BREWING, gl.PHASE_CRAFTED)
                                  and len(st.selected) > 0)
        self.btn_clear.draw(self.screen, mouse_pos)
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
        draw_text(self.screen, f"+{res['gold']} Gold", self.font_lg,
                  (242, 201, 76), WIDTH // 2, ty + 50, center=True)

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
        self.btn_advance.draw(self.screen, mouse_pos)


if __name__ == "__main__":
    Game().run()
