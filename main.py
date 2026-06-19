import pygame
from assets.components.PotionStorage import PotionStorage
from assets.components.Customer import Customer
from assets.components.ImageButton import ImageButton
from assets.components.Ingredient import Ingredient

SCREEN_SIZE = (1600, 900)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("소환사 주문가게에 오신 여러분, 환영합니다.")
clock = pygame.time.Clock()

background = pygame.image.load("./assets/images/backgrounds/game_play_bg.png").convert()
background = pygame.transform.smoothscale(background, SCREEN_SIZE)

pot = pygame.image.load("./assets/images/ingredients/pot.png").convert_alpha()
pot = pygame.transform.smoothscale(pot, (375, 370))
#####################
customer = Customer(screen)
storage1 = PotionStorage(screen, 1000)
storage2 = PotionStorage(screen, 1200)

ingredient_combination_list = [False] * 10
print(ingredient_combination_list)

ingredients = []
for i in range(0, 10):
    # i번 쟤료 이미지버튼 만들기
    temp = Ingredient(screen, i, ingredient_combination_list)
    ingredients.append(temp)

# poison = 
potion = None
def make_potion():
    global potion
    # 조합법 하드코딩
    Red = [False, True, False, False, True,
        False, False, False, True, False]
    Green = [False, False, False, True, False,
        True, False, True, False, False]
    Blue = [False, False, False, True, False,
        False, True, False, False, True]
    Purple = [True, True, True, False, False,
        False, False, False, False, False]
    if ingredient_combination_list == Red:
        potion = "Red"
    elif ingredient_combination_list == Green:
        potion = "Green"
    elif ingredient_combination_list == Blue:
        potion = "Blue"
    elif ingredient_combination_list == Purple:
        potion = "Purple"
    else: potion = None

#####################

running = True
frame_count = 0

while running:
    dt = clock.tick(100) # 100FPS
    frame_count += 1
    # if frame_count % 100 == 0: print(frame_count)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 재료 버튼들 클릭 판단
                for ingredient in ingredients:
                    ingredient.update_event()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                customer.give_job()

        
    # 화면 업데이트
    screen.blit(background, (0, 0)) # 배경
    storage1.update()
    customer.update()
    screen.blit(pot, (605, 467)) # 가마솥
    for ingredient in ingredients:
        ingredient.update()

    pygame.display.flip() # update() 랑 똑같은 기능, update(Rect)로 Rect 범위만 업데이트 가능
pygame.quit()