import pygame

class Button:
    def __init__(self, x: int|float, y: int|float, width: int|float, height: int|float, text: str = "") -> pygame.Rect:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("None", 30)
        self.Text = self.font.render(text, True, (255, 255, 255))

        self.Rect = pygame.Rect(x, y, width, height)
        return self.Rect # 이거 안쓸것같긴해
    
    def is_in(self, mouse_x, mouse_y):
        # 마우스의 좌표가 버튼 안에 있는지 감지. ( 버튼 클릭 감지 )
        if (self.x <= mouse_x <= self.x + self.width) and (self.y <= mouse_y <= self.y + self.height):
            return True
        #else:
        return False