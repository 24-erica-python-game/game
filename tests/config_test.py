from src.utils.config import Config, Font, FontData
from dataclasses import asdict
# from dacite import from_dict

from utils.config import Display


def test_config():
    config = Config(
        Font([FontData("default", "malgungothic", 18)]),
        Display(
            Display.WindowSize(
                available={
                    "1920x1080": [1920, 1080]
                },
                current="1920x1080"
            ),
            vsync=True
        )
    )
    d = asdict(config)
    Config.set_config(d)
    Config.set_config(False, "display.vsync")
    d["display"]["vsync"] = False
    assert d == Config.get_config()
    # assert from_dict(Config, Config.get_config()) == config


#Config(font=Font(fonts=[FontData(name='default', font='malgungothic', size=16)]), display=Display(window_size=Display.WindowSize(available={'1920x1080': [1920, 1080]}, current='1920x1080'), vsync=False, framerate=60, display=0))
#Config(font=Font(fonts=[FontData(name='default', font='malgungothic', size=16)]), display=Display(window_size=Display.WindowSize(available={'1920x1080': [1920, 1080]}, current='1920x1080'), vsync=False, framerate=60, display=0))
