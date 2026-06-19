import pygame
import random

NEEDS = [
    "Red", "Green", "Blue", "Purple"
]

IMAGE_SIZE = (300, 400)

class Customer:
    def __init__(self, screen: pygame.display.Surface):
        self.screen = screen
        self.need = "None"
        self.is_hanul = False
        self.Image = None
        self.need_Image = None

        self.give_job()

        print("Hello, world!")
    
    def give_job(self):
        self.is_hanul = True if random.randint(1, 100) <= 25 else False # 25% 확률로 한울이임
        self.need = random.choice(NEEDS)
        
        self.need_Image = pygame.image.load(f"assets/images/potions/{self.need.lower()}.png").convert_alpha()
        self.need_Image = pygame.transform.smoothscale(self.need_Image, (115, 180))
        
        self.Image = pygame.image.load(f"assets/images/customers/{random.randint(0, 1)}.png").convert() # 김주영/김우찬 사진 랜덤고름
        self.Image = pygame.transform.smoothscale(self.Image, IMAGE_SIZE)

        if self.is_hanul: # 장한울이면 이름, 사진 변경
            self.name = "장한울"
            self.Image = pygame.image.load(f"assets/images/customers/hanuls/{random.randint(0, 11)}.jpg").convert() # 장징궈사진만 jpg임!!!
            self.Image = pygame.transform.smoothscale(self.Image, IMAGE_SIZE)
        
    def update(self):
        self.screen.blit(self.Image, (530, 235))
        self.screen.blit(self.need_Image, (530+IMAGE_SIZE[0] + 10, 235))