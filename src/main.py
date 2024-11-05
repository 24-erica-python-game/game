import pygame as pg

from game.scene.game.in_game import GameScene
from src.game.scene.home import HomeScene
from utils.config import Config

pg.init()  # 게임 엔진 초기화

running = True
clock = pg.time.Clock()

# 디스플레이 설정
display_config = Config.get_config("display")
current_size = display_config["window_size"]["current"]
size = Config.get_config(f"display.window_size.available.{current_size}")
framerate = display_config["framerate"]
vsync = display_config["vsync"]
screen = pg.display.set_mode(size, vsync=vsync)

pg.display.set_caption("Buggy Buddies")  # 창 상단 캡션 설정

home_scene = HomeScene()
game_scene = GameScene("test_map_1")

while running:
    clock.tick(framerate)

    # pygame.event.get() 함수를 통해 게임 중간에 발생한 이벤트를 캐치하여 검사하기 위한 인덱스로 사용
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                running = False

    screen.fill((255, 255, 255))

    game_scene.draw()

    pg.display.flip() # pygame의 메인 루프 끝에 반드시 사용
