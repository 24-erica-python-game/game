import pygame as pg

pg.init() #게임 엔진 초기화

#RGB 색 지정
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

#화면 크기 지정
size = [1280, 800]
screen = pg.display.set_mode(size)

pg.display.set_caption("Buggy Buddies")

#FPS 관련 설정
done = False
clock = pg.time.Clock()

while not done:
    clock.tick(30) # 10프레임 / 너무 높으면 CPU많이 먹으니까 10,30,60이 적당

    for event in pg.event.get(): #pygame.event.get() 함수를 통해 게임 중간에 발생한 이벤트를 캐치하여 검사하기 위한 인덱스로 사용
        if event.type == pg.QUIT: # 종료시 실행
            done = True


    screen.fill(WHITE)


    pg.draw.polygon(screen, GREEN, [[30, 150], [125, 100], [220, 150]], 5)
    pg.draw.polygon(screen, GREEN, [[30, 150], [125, 100], [220, 150]], 0)
    pg.draw.lines(screen, RED, False, [[50, 150], [50, 250], [200, 250], [200, 150]], 5)
    pg.draw.rect(screen, BLACK, [75, 175, 75, 50], 5)
    pg.draw.rect(screen, BLUE, [75, 175, 75, 50], 0)
    pg.draw.line(screen, BLACK, [112, 175], [112, 225], 5)
    pg.draw.line(screen, BLACK, [75, 200], [150, 200], 5)


    pg.display.flip() #pygame의 메인 루프 끝에 반드시 사용

