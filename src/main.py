import pygame as pg

from game.tile import TileMap

pg.init() #게임 엔진 초기화

#RGB 색 지정
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

#화면 크기 지정
x = 1280
y = 800
size = [x, y]
screen = pg.display.set_mode(size)

pg.display.set_caption("Buggy Buddies")

#FPS 관련 설정
running = True
tile_map = TileMap()
clock = pg.time.Clock()

while running:
    clock.tick(30) # 30프레임 / 너무 높으면 CPU많이 먹으니까 10,30,60이 적당

    for event in pg.event.get(): #pygame.event.get() 함수를 통해 게임 중간에 발생한 이벤트를 캐치하여 검사하기 위한 인덱스로 사용
        match (event.type):
            case pg.QUIT:
                running = False


    screen.fill(WHITE)

    pg.draw.rect(screen, BLACK, [0,0,1280,50])
    pg.draw.rect(screen, BLACK, [0,650,1280,150])


    pg.display.flip() #pygame의 메인 루프 끝에 반드시 사용

