import pygame as pg

from game.tile import TileMap

pg.init() #게임 엔진 초기화

#RGB 색 지정
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

#글자 폰트 지정
font = pg.font.SysFont("malgungothic", 18, False, False) #(font name, size, bold, italic)
small_font = pg.font.SysFont("malgungothic", 14, False, False)

#화면 크기 지정
size = [1280, 800]
screen = pg.display.set_mode(size)

pg.display.set_caption("Buggy Buddies")

#FPS 관련 설정
running = True
tile_map = TileMap()
clock = pg.time.Clock()

#TODO:임시적으로 생성한 변수로 추후에 다른 파일로 옮겨야 할듯
active_point = 100
player_hp = 100
supply = 1000
player_power = 50

game_info = font.render("게임 정보", True, BLACK) #(Text, antialias,color, background color)
minimap = font.render("미니맵", True, BLACK)

#유닛정보 표시내용
unit_info = font.render("유닛 정보", True, BLACK)
active_point_info = font.render("활동력: {}".format(active_point), True, BLACK)
player_hp_info = font.render("체력: {}".format(player_hp), True, BLACK)
supply_info = font.render("보급량: {}".format(supply), True, BLACK)
player_power_info = font.render("공격력: {}".format(player_power), True, BLACK)

while running:
    clock.tick(30) # 30프레임 / 너무 높으면 CPU많이 먹으니까 10,30,60이 적당

    for event in pg.event.get(): #pygame.event.get() 함수를 통해 게임 중간에 발생한 이벤트를 캐치하여 검사하기 위한 인덱스로 사용
        match (event.type):
            case pg.QUIT:
                running = False


    screen.fill(WHITE)

    pg.draw.rect(screen, GREEN, [0,0,1280,50]) #게임정보
    pg.draw.rect(screen, GREEN, [0,650,150,150]) #맵
    pg.draw.rect(screen, GREEN, [1080,650,200,150]) #유닛
    
    screen.blit(game_info, (640, 10))
    screen.blit(minimap, (50,700))

    screen.blit(unit_info,(1150, 650))
    pg.draw.line(screen, BLACK, (1080,675),(1280,675))
    screen.blit(active_point_info, (1100,690))
    screen.blit(player_hp_info, (1100,710))
    screen.blit(supply_info, (1100,730))
    screen.blit(player_power_info, (1100,750))

    pg.display.flip() #pygame의 메인 루프 끝에 반드시 사용
print(pg.font.get_fonts())