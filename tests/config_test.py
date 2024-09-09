from src.utils.config import Config, Font
from dacite import from_dict


def test_config():
    Config.set_config(13.0, "font.default_size")
    assert from_dict(Config, Config.get_config()) == Config(Font("malgungothic", 13.0))
