import pygame

class ImageButton:
    def __init__(self, screen: pygame.display.Surface, \
        img_path: pygame.Surface, \
        x: int|float, y: int|float, w: int|float, h: int|float, \
        func = lambda: print(f"I'm pressed."), \
        is_checkbox: bool = False):
        self.screen = screen

        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (w, h))

        self.hover_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.hover_image.fill((0, 0, 0, 100)) # alpha: 0-255
        self.hover_image.blit(self.image, (0, 0))

        self.checked_hover_image = pygame.Surface(self.hover_image.get_size(), pygame.SRCALPHA)
        self.checked_hover_image.fill((0, 0, 0, 100))
        self.checked_hover_image.blit(self.hover_image, (0, 0))

        self.checked_image = self.hover_image
        # # hover 이미지 재사용하면 될듯?
        # self.checked_image = pygame.Surface(self.hover_image.get_size(), pygame.SRCALPHA)
        # self.checked_image.fill((0, 0, 0, 100))
        # self.checked_image.blit(self.hover_image, (0, 0))
        
        self.Rect = self.image.get_rect()
        self.Rect.topleft = (x, y)

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.func = func

        self.is_checkbox = is_checkbox
        self.is_checked = False

    # 마우스가 버튼 안에 있는지 판단하는 함수
    def is_mouse_in(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.x <= mouse_x <= self.x + self.w and \
            self.y <= mouse_y <= self.y + self.h:
            # 마우스 좌표가 버튼 내부에 있음 => 클릭
            return True
        return False
    
    # 화면에 그리기
    def update(self):
        update_image = None
        if self.is_mouse_in(): # 호버링 된 이미지 띄우기
            if self.is_checked: update_image = self.checked_hover_image
            else: update_image = self.hover_image
        else:
            if self.is_checked: update_image = self.checked_image
            else: update_image = self.image
        self.screen.blit(update_image, self.Rect)
    def update_event(self):
        if self.is_mouse_in():
            self.func()
            
            if self.is_checkbox:
                self.is_checked = not self.is_checked

            # print(self.is_checked)