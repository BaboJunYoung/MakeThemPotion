import pygame
from assets.components.ImageButton import ImageButton

MAX_HEIGHT = 635
SIDE_LENGTH = 130

class Ingredient:
    def __init__(self, screen: pygame.display.Surface, ingredient_type: int, ingredient_list: list):
        self.screen = screen
        self.type = ingredient_type
        self.ingredient_list = ingredient_list
        
        def func():
            self.ingredient_list[self.type] = not self.ingredient_list[self.type]
            print(self.ingredient_list)

        x_pos, y_pos = self.__get_right_position()
        self.ImageButton = ImageButton(screen, \
            f"assets/images/ingredients/{ingredient_type}.png", \
            x_pos, y_pos, SIDE_LENGTH, SIDE_LENGTH, \
            func, is_checkbox=True)
    
    # 재료 타입에 맞는 올바른 위치 반환. (MAX_HEIGHT, SIDE_LENGTH를 통해 올바른 위치를 수학적으로 계산)
    def __get_right_position(self):
        """
        0 1 2 3 4
        5 6 7 8 9
        """
        x_pos = 0 + SIDE_LENGTH * (self.type % 5)
        y_pos = MAX_HEIGHT + SIDE_LENGTH * (self.type // 5)

        return (x_pos, y_pos)
    
    def update(self):
        self.ImageButton.update()
    def update_event(self):
        self.ImageButton.update_event()