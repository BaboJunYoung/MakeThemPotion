import pygame


SCREEN_SIZE = (800, 600)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("소환사 주문가게에 오신 여러분, 환영합니다.")
clock = pygame.time.Clock()


# background = pygame.image.load("./assets/images/game_play_bg.png")
background = pygame.image.load("./assets/images/game_intro_bg.png")

running = True

while running:
    dt = clock.tick(60) # 60FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # 좌: 1
            # 휠: 2
            # 우: 3
            if event.button == 1: # 좌클릭
                print("hello world!")