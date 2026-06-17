"""Reusable visual-novel style dialogue presentation for Potion Workshop.

The game can use this module before final dialogue-box and character art exists.
It supports:

- speaker name + dialogue body
- click/Enter advancement
- smooth ease-in-out fade/slide transitions
- replaceable dialogue box image
- character slots with fade-in and slight upward motion
"""

from dataclasses import dataclass

import pygame


def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def ease_in_out_cubic(t):
    """Smooth cubic easing for UI motion."""
    t = clamp(t)
    if t < 0.5:
        return 4 * t * t * t
    return 1 - pow(-2 * t + 2, 3) / 2


def smootherstep(t):
    """Ken Perlin's smootherstep: zero 1st/2nd derivatives at the ends.

    Gives the per-character reveal a soft, wave-like rise instead of a
    mechanical pop-in.
    """
    t = clamp(t)
    return t * t * t * (t * (t * 6 - 15) + 10)


@dataclass
class DialogueLine:
    speaker: str
    text: str
    character_slot: str | None = "left"
    character_color: tuple[int, int, int] = (110, 90, 140)
    character_image: pygame.Surface | None = None
    background_image: pygame.Surface | None = None
    sound_effect: pygame.mixer.Sound | None = None


class CharacterActor:
    """A future-proof character stand-in.

    If image is provided, it is rendered. Otherwise a simple translucent
    placeholder silhouette is drawn so the dialogue layout can be tuned now.
    """

    def __init__(self, slot, rect, name="", image=None, color=(110, 90, 140)):
        self.slot = slot
        self.rect = pygame.Rect(rect)
        self.name = name
        self.image = image
        self.color = color
        self.enter_time = 0.0
        self.duration = 0.42
        self.visible = True

    def set(self, name, image=None, color=(110, 90, 140)):
        changed = self.image is not image or self.color != color
        self.name = name
        self.image = image
        self.color = color
        self.visible = True
        if changed:
            self.enter_time = 0.0

    def update(self, dt):
        if self.visible:
            self.enter_time = min(self.duration, self.enter_time + dt)

    def draw(self, surf):
        if not self.visible:
            return

        progress = ease_in_out_cubic(self.enter_time / self.duration)
        alpha = int(255 * progress)
        y_offset = int(28 * (1.0 - progress))
        rect = self.rect.move(0, y_offset)

        layer = pygame.Surface(rect.size, pygame.SRCALPHA)
        if self.image:
            source = self.image
            mask = pygame.mask.from_surface(source, 8)
            bounds = mask.get_bounding_rects()
            if bounds:
                crop_rect = bounds[0].copy()
                for rect_part in bounds[1:]:
                    crop_rect.union_ip(rect_part)
                source = source.subsurface(crop_rect).copy()

            src_w, src_h = source.get_size()
            scale = min(rect.width / src_w, rect.height / src_h)
            size = (max(1, int(src_w * scale)), max(1, int(src_h * scale)))
            img = pygame.transform.smoothscale(source, size)
            img.set_alpha(alpha)
            layer.blit(img, img.get_rect(midbottom=(rect.width // 2, rect.height)))
        else:
            body = pygame.Rect(rect.width // 2 - 48, 92, 96, rect.height - 108)
            head_center = (rect.width // 2, 54)
            pygame.draw.ellipse(layer, (*self.color, max(0, alpha - 35)), body)
            pygame.draw.circle(layer, (235, 210, 180, alpha), head_center, 38)
            pygame.draw.circle(layer, (60, 48, 40, alpha), head_center, 38, 2)
        surf.blit(layer, rect)


class DialogueController:
    def __init__(
        self,
        screen_width,
        screen_height,
        font_name=None,
        font_path=None,
        name_size=22,
        body_size=24,
        next_size=16,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_name = font_name or "malgungothic,applegothic,notosanscjkkr,gulim,arial"
        if font_path:
            self.name_font = pygame.font.Font(font_path, name_size)
            self.name_font.set_bold(True)
            self.body_font = pygame.font.Font(font_path, body_size)
            self.next_font = pygame.font.Font(font_path, next_size)
        else:
            self.name_font = pygame.font.SysFont(self.font_name, name_size, bold=True)
            self.body_font = pygame.font.SysFont(self.font_name, body_size)
            self.next_font = pygame.font.SysFont(self.font_name, next_size)

        self.box_rect = pygame.Rect(60, screen_height - 190, screen_width - 120, 150)
        self.box_image = None
        self.lines = []
        self.index = 0
        self.visible = False
        self.finished = False
        self.hide_on_finish = False
        self.closing = False
        self.transition_time = 0.0
        self.transition_duration = 0.38
        self.close_time = 0.0
        self.close_duration = 0.34
        self.type_time = 0.0
        self.chars_per_second = 26.0
        self.char_rise = 8
        self.reveal_window = 5.2   # 한 글자가 물결처럼 떠오르는 데 걸리는 글자 수
        self.line_height = max(body_size + 9, 33)
        # 모든 레이아웃은 대화 상자 크기에 대한 비율(0~1)로 표현해
        # 박스 이미지를 어떤 크기로 그려도 글자/이름 위치가 함께 맞춰진다.
        self.name_anchor = (0.165, 0.165)   # 이름판 중앙
        self.text_origin = (0.06, 0.36)     # 본문 좌상단
        self.text_width_frac = 0.88
        self.prompt_margin_frac = (0.035, 0.07)
        self.typewriter = True
        self.type_sound = None
        self.type_sound_interval = 2
        self.type_sound_volume = 0.45
        self.last_sound_step = 0
        self.current_key = None

        self.actors = {
            "left": CharacterActor("left", (35, 105, 220, 330)),
            "center": CharacterActor("center", (screen_width // 2 - 120, 95, 240, 350)),
            "right": CharacterActor("right", (screen_width - 255, 105, 220, 330)),
        }

    def set_box_rect(self, rect):
        self.box_rect = pygame.Rect(rect)

    def set_box_image(self, image):
        self.box_image = image

    def set_visual_style(
        self,
        name_anchor=None,
        text_origin=None,
        text_width_frac=None,
        line_height=None,
        prompt_margin_frac=None,
        char_rise=None,
        chars_per_second=None,
        reveal_window=None,
    ):
        """레이아웃 미세조정. 위치 값은 모두 박스 크기 대비 비율(0~1)."""
        if name_anchor is not None:
            self.name_anchor = name_anchor
        if text_origin is not None:
            self.text_origin = text_origin
        if text_width_frac is not None:
            self.text_width_frac = text_width_frac
        if line_height is not None:
            self.line_height = line_height
        if prompt_margin_frac is not None:
            self.prompt_margin_frac = prompt_margin_frac
        if char_rise is not None:
            self.char_rise = char_rise
        if chars_per_second is not None:
            self.chars_per_second = chars_per_second
        if reveal_window is not None:
            self.reveal_window = reveal_window

    def current_line(self):
        return self._current_line()

    def set_type_sound(self, sound, interval=2, volume=0.45):
        self.type_sound = sound
        self.type_sound_interval = max(1, interval)
        self.type_sound_volume = volume
        if self.type_sound:
            self.type_sound.set_volume(volume)

    def set_actor_rect(self, slot, rect):
        if slot in self.actors:
            self.actors[slot].rect = pygame.Rect(rect)

    def set_script(self, lines, key=None, hide_on_finish=False):
        """Replace the current script unless the key is unchanged."""
        if key is not None and key == self.current_key:
            return

        self.lines = [
            line if isinstance(line, DialogueLine) else DialogueLine(**line)
            for line in lines
        ]
        self.index = 0
        self.visible = bool(self.lines)
        self.finished = False
        self.closing = False
        self.hide_on_finish = hide_on_finish
        self.current_key = key
        self._restart_transition()
        self.type_time = 0.0
        self._sync_actor_to_line()

    def clear(self):
        self.lines = []
        self.visible = False
        self.finished = True
        self.closing = False
        self.current_key = None

    def close(self):
        if not self.visible or self.closing:
            return
        self.closing = True
        self.close_time = 0.0

    def _restart_transition(self):
        self.transition_time = 0.0
        self.close_time = 0.0
        self.type_time = 0.0
        self.last_sound_step = 0

    def _restart_text(self):
        self.type_time = 0.0
        self.last_sound_step = 0

    def _current_line(self):
        if not self.visible or not self.lines:
            return None
        return self.lines[self.index]

    def _sync_actor_to_line(self):
        line = self._current_line()
        if not line:
            return
        if line.character_slot == "keep":
            return
        if line.character_slot is None:
            # 캐릭터 없는 라인(나레이션/CG)에서는 이전 캐릭터가 남지 않게 모두 숨긴다.
            for actor in self.actors.values():
                actor.name = ""
                actor.visible = False
            return
        for slot, actor in self.actors.items():
            if slot != line.character_slot:
                actor.name = ""
                actor.visible = False
        actor = self.actors.get(line.character_slot)
        if actor:
            actor.set(line.speaker, image=line.character_image, color=line.character_color)

    def _visible_character_count(self):
        line = self._current_line()
        if not line:
            return 0
        if not self.typewriter:
            return len(line.text)
        return min(len(line.text), int(self.type_time * self.chars_per_second))

    def is_line_complete(self):
        line = self._current_line()
        return not line or self._visible_character_count() >= len(line.text)

    def complete_line(self):
        line = self._current_line()
        if line:
            # +0.5 글자만큼 여유를 둬 부동소수점 절삭으로 마지막 글자가
            # 안 드러나 is_line_complete() 가 영영 False 가 되는 일을 막는다.
            self.type_time = (len(line.text) + 0.5) / self.chars_per_second
            self.last_sound_step = len(line.text) // self.type_sound_interval

    def advance(self):
        """Move to the next line. Returns True when the script has finished."""
        if not self.visible or not self.lines or self.closing:
            return False

        if not self.is_line_complete():
            self.complete_line()
            return False

        if self.index < len(self.lines) - 1:
            old_speaker = self._current_line().speaker
            self.index += 1
            new_speaker = self._current_line().speaker
            self._restart_text()
            if old_speaker != new_speaker:
                self.transition_time = 0.0
            self._sync_actor_to_line()
            return False

        if self.hide_on_finish:
            self.closing = True
            self.close_time = 0.0
            return False
        self.finished = True
        return True

    def handle_event(self, event):
        if not self.visible or self.closing:
            return False
        if self.finished and not self.hide_on_finish:
            return False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.advance()
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.advance()
            return True
        return False

    def update(self, dt):
        if not self.visible:
            return
        if self.closing:
            self.close_time = min(self.close_duration, self.close_time + dt)
            if self.close_time >= self.close_duration:
                self.visible = False
                self.finished = True
            return

        self.transition_time = min(self.transition_duration, self.transition_time + dt)
        self.type_time += dt
        self._play_type_sound_if_needed()
        for actor in self.actors.values():
            actor.update(dt)

    def _play_type_sound_if_needed(self):
        if not self.type_sound or not self.typewriter:
            return

        visible_count = self._visible_character_count()
        if visible_count <= 0:
            return

        step = visible_count // self.type_sound_interval
        if step > self.last_sound_step:
            try:
                self.type_sound.play()
            except pygame.error:
                pass
        self.last_sound_step = step

    def draw(self, surf):
        if not self.visible:
            return

        line = self._current_line()
        if not line:
            return

        for actor in self.actors.values():
            if actor.name:
                actor.draw(surf)

        progress = ease_in_out_cubic(self.transition_time / self.transition_duration)
        close_progress = ease_in_out_cubic(self.close_time / self.close_duration) if self.closing else 0
        alpha = int(232 * progress * (1.0 - close_progress))
        y_offset = int(26 * (1.0 - progress) + 24 * close_progress)
        box = self.box_rect.move(0, y_offset)

        bw, bh = box.size
        layer = pygame.Surface(box.size, pygame.SRCALPHA)
        if self.box_image:
            # 박스 이미지는 box_rect 와 같은 가로세로 비율로 들어오므로 늘어나지 않는다.
            img = pygame.transform.smoothscale(self.box_image, box.size)
            img.set_alpha(alpha)
            layer.blit(img, (0, 0))
        else:
            pygame.draw.rect(layer, (32, 24, 22, alpha), layer.get_rect(), border_radius=16)
            pygame.draw.rect(layer, (212, 175, 99, alpha), layer.get_rect(), 2, border_radius=16)

        # 이름은 박스 이미지에 이미 있는 이름판 위에 글자만 얹는다 (별도 배경 없음).
        name = self.name_font.render(line.speaker, True, (236, 226, 248))
        name.set_alpha(alpha)
        nx, ny = self.name_anchor
        layer.blit(name, name.get_rect(center=(int(bw * nx), int(bh * ny))))

        tx, ty = self.text_origin
        self._draw_typewriter_text(
            layer,
            line.text,
            alpha,
            int(bw * self.text_width_frac),
            int(bw * tx),
            int(bh * ty),
        )

        prompt = "클릭 / Enter" if self.is_line_complete() else "..."
        prompt_img = self.next_font.render(prompt, True, (230, 214, 170))
        prompt_img.set_alpha(150 + int(70 * abs((pygame.time.get_ticks() % 900) / 450 - 1)))
        px, py = self.prompt_margin_frac
        layer.blit(prompt_img, (bw - prompt_img.get_width() - int(bw * px),
                                bh - prompt_img.get_height() - int(bh * py)))

        surf.blit(layer, box)

    def _draw_typewriter_text(self, surf, text, alpha, max_width, x, y):
        line_height = self.line_height
        head = self.type_time * self.chars_per_second   # 현재 드러나는 위치(글자 단위)
        window = self.reveal_window
        char_index = 0
        cursor_x = x
        cursor_y = y

        for paragraph in text.split("\n"):
            for token in self._tokenize_for_wrap(paragraph):
                token_width = self.body_font.size(token)[0]
                if token != " " and cursor_x > x and cursor_x + token_width > x + max_width:
                    cursor_x = x
                    cursor_y += line_height

                for ch in token:
                    ch_width = self.body_font.size(ch)[0]
                    if ch != " " and cursor_x > x and cursor_x + ch_width > x + max_width:
                        cursor_x = x
                        cursor_y += line_height

                    # 각 글자는 앞 글자보다 한 박자 늦게, 넓은 창(window)에 걸쳐
                    # 떠오르므로 여러 글자가 동시에 움직이며 물결처럼 보인다.
                    age = head - char_index
                    if age > 0:
                        eased = smootherstep(age / window)
                        ripple = 1.5 * (1.0 - eased) * smootherstep(age / (window * 0.7))
                        rise = self.char_rise * (1.0 - eased) + ripple
                        ch_img = self.body_font.render(ch, True, (240, 232, 218))
                        ch_img.set_alpha(int(alpha * eased))
                        surf.blit(ch_img, (cursor_x, cursor_y + rise))

                    cursor_x += ch_width
                    char_index += 1
            cursor_x = x
            cursor_y += line_height

    @staticmethod
    def _tokenize_for_wrap(text):
        tokens = []
        current = ""
        for ch in text:
            if ch == " ":
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(ch)
            else:
                current += ch
        if current:
            tokens.append(current)
        return tokens

    @staticmethod
    def _wrap_text(text, font, max_width):
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
            if current:
                lines.append(current)
        return lines
