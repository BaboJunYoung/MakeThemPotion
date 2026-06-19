import pygame

class Text:
    def __init__(self, screen: pygame.display.Surface, text:str, font_size = 30):
        self.screen = screen
        self.font = pygame.font.SysFont(None, font_size)
        self.Surface = self.font.render(text, True, (255, 255, 255))
    
    def update(self, x, y):
        self.screen.blit(self.Surface, (x, y))