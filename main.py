import pygame


SCREEN_SIZE = (800, 600)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("소환사 주문가게에 오신 여러분, 환영합니다.")
clock = pygame.time.Clock()


background_original = pygame.image.load("./assets/images/game_play_bg.png")
background = pygame.transform.smoothscale(background_original, SCREEN_SIZE)
# background = pygame.image.load("./assets/images/game_intro_bg.png")

running = True

while running:
    dt = clock.tick(60) # 60FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        elif event.type == pygame.VIDEORESIZE:
            new_width = event.w
            new_height = event.h

            # screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

            background = pygame.transform.scale(background_original, (new_width, new_height))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 좌: 1
            # 휠: 2
            # 우: 3
            if event.button == 1: # 좌클릭
                print("hello world!")
        

    # 화면 업데이트
    screen.blit(background, (0, 0)) # 배경
    
    pygame.display.flip() # update() 랑 똑같은 기능, update(Rect)로 Rect 범위만 업데이트 가능

pygame.quit()