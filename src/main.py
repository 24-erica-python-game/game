import pygame as pg

from game.scene.home import HomeScene
from game.scene.in_game import GameScene
from utils.config import Config

pg.init()  # 게임 엔진 초기화

running = True
clock = pg.time.Clock()

font = pg.font.SysFont("malgungothic", 18, False, False)  # (font name, size, bold, italic)
small_font = pg.font.SysFont("malgungothic", 14, False, False)

display_config = Config.get_config("display")
size = display_config["window_size"]["current"]
size = Config.get_config(f"display.window_size.available.{size}")
framerate = display_config["framerate"]
vsync = display_config["vsync"]
screen = pg.display.set_mode(size, vsync=vsync)

pg.display.set_caption("Buggy Buddies")


current_scene: str = "home"
scenes = {
    "home": HomeScene(),
}

while running:
    clock.tick(framerate)  # 30프레임 / 너무 높으면 CPU많이 먹으니까 10,30,60이 적당

    for event in pg.event.get():  # pygame.event.get() 함수를 통해 게임 중간에 발생한 이벤트를 캐치하여 검사하기 위한 인덱스로 사용
        match event.type:
            case pg.QUIT:
                running = False

    match current_scene:
        case "home":
            scenes["home"].run()
        # case "game":
        #     GameScene.run()

    pg.display.flip() #pygame의 메인 루프 끝에 반드시 사용
