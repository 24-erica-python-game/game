from src.utils.config import Config, Font


def test_config():
    Config.set_config(13.0, "font.default_size")
    assert Config.get_config() == Config(Font("malgungothic", 13.0))
