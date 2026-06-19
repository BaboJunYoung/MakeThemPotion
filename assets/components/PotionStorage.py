import pygame
from assets.components.ImageButton import ImageButton

class PotionStorage:
    def __init__(self, screen: pygame.display.Surface, x: int|float):
        self.ImageButton = ImageButton(screen, "assets/images/potions/save.png", x, 700, 140, 140)
        self.storaging_potion_Image = None
        self.storaging_potion = "None"
    
    # 포션 저장됨 여부
    def storage(self, potion: str) -> bool:
        if self.storaging_potion != "None": # 이미 포션이 있음
            return False
        self.storaging_potion = potion
        self.storaging_potion_Image = pygame.image.load(f"assets/images/potions/{potion.lower()}.png")

        return True
    
    # 저장된 포션 빼오기
    def pop_storaging_potion(self) -> str | bool:
        if self.storaging_potion == "None": # 비어있는데 어케 가져가게
            return False

        temp = self.storaging_potion
        self.storaging_potion = "None"
        return temp
    
    # 화면에 그리기
    def update(self):
        self.ImageButton.update()