import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any

import pygame as pg
from dacite import from_dict
from pygame.font import FontType


_config_path = os.path.normpath(f"{os.getcwd()}/data/config.json")


class OnKeyErrorBehavior(Enum):
    ReturnNone = 0
    RaiseError = 1


@dataclass
class FontData:
    name: str
    font: str
    size: int


@dataclass
class Font:
    fonts: list[FontData]

    @staticmethod
    def get_font(name: str, fonts: list) -> FontType:
        """
        폰트 데이터 목록에서 폰트를 검색한 결과를 반환함.
        :param name: 폰트 데이터의 이름
        :param fonts: 폰트 목록, 일반적으로 ``Config.get_config("font.fonts")`` 가 들어감.
        :raises ValueError: 해당 폰트를 찾지 못했을 경우
        :return:
        """
        _fonts = [from_dict(FontData, font) for font in fonts]
        for font in _fonts:
            if font.name == name:
                return pg.font.SysFont(font.font, font.size, False, False)
        raise ValueError(f"Font not found: {name}")


type _display_size = list[int]
# type _display_mode = Literal["w", "bw", "f"]

@dataclass
class Display:
    @dataclass
    class WindowSize:
        available: dict[str, list[int]]
        current: str

    window_size: WindowSize
    vsync: bool = False
    framerate: int = 60
    display: int = 0


@dataclass
class Config:
    font: Font
    display: Display

    @staticmethod
    def get_config(index: Optional[str] = None,
                   delimiter: str = '.',
                   on_key_error: OnKeyErrorBehavior = OnKeyErrorBehavior.ReturnNone) -> Any:
        """
        data/config.json의 값을 가져옴.

        >>> config = {
        ...     "foo": {
        ...         "bar": 10,
        ...         "baz": 40
        ...     }
        ... }

        >>> Config.get_config()
        {'foo': {'bar': 10, 'baz': 40}}

        >>> Config.get_config("foo.baz")
        40

        >>> Config.get_config("foo/bar", delimiter='/')
        10

        :param index: 접근할 인덱스, ``delimiter`` 값을 기준으로 ``str.split()`` 을 수행함
        :param delimiter: 인덱스를 나눌 구분자
        :param on_key_error: 인덱스를 찾을 수 없을 경우 처리할 행동
        :raises KeyError: 인덱스를 찾을 수 없으며 ``on_key_error`` 가 ``RaiseError`` 로 설정되어있을 경우
        :raises FileNotFoundError: 파일이 없는 경우
        :return: 찾은 결과, 만약 인덱스를 찾지 못했으며 ``on_key_error`` 가 ``ReturnNone`` 일 경우 ``None`` 이 리턴됨
        """
        with open(_config_path, 'r') as f:
            config: dict = json.load(f)
            if index is None:
                result = config
            else:
                index_list = index.split(delimiter)
                v = config
                try:
                    for i in index_list:
                        v = v[i]
                    result = v
                except KeyError as e:
                    match on_key_error:
                        case OnKeyErrorBehavior.ReturnNone:
                            return None
                        case OnKeyErrorBehavior.RaiseError:
                            raise KeyError(e)
            return result

    @staticmethod
    def set_config(value, index: Optional[str] = None, delimiter: str = '.'):
        """
        ``data/config.json`` 의 값을 가져온 후 ``index`` 의 값을 ``value`` 로 설정함.

        >>> config = {
        ...     "foo": {
        ...         "bar": 10,
        ...         "baz": 40
        ...     }
        ... }

        >>> Config.get_config()
        {'foo': {'bar': 10, 'baz': 40}}

        >>> Config.set_config(20, "foo.bar")

        >>> Config.get_config()
        {'foo': {'bar': 20, 'baz': 40}}

        :param value: 설정할 값
        :param index: 접근할 인덱스
        :param delimiter: 인덱스를 나눌 구분자
        :raises KeyError: 인덱스를 찾을 수 없을 경우
        """
        if index is not None:
            index_list = index.split(delimiter)
            config_data = Config.get_config(on_key_error=OnKeyErrorBehavior.RaiseError)
            temp = config_data
            for idx in index_list[:-1]:  # config_data의 참조인 상태를 유지하기 위해 [:-1]을 함
                temp = temp[idx]
            temp[index_list[-1]] = value  # temp는 config_data의 참조이므로 config_data의 값이 변경됨
            value = config_data
        with open(_config_path, 'w') as f:
            json.dump(value, f, indent=4)
