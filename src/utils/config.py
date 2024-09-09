import json
from dataclasses import dataclass
from typing import Optional
from dacite import from_dict

@dataclass
class Font:
    default_font: str = "malgungothic"
    default_size: float = 18.0

@dataclass
class Config:
    font: Font

    @staticmethod
    def get_config(index: Optional[str] = None, delimiter: str = '.'):
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

        :param index: 접근할 인덱스, delimiter 값을 기준으로 str.split()을 수행함
        :param delimiter: 인덱스를 나눌 구분자
        :raises KeyError: 인덱스를 찾을 수 없을 경우
        :raises FileNotFoundError: 파일이 없는 경우
        :return: Config의 인스턴스
        """
        with open("config.json", 'r') as f:
            config: dict = json.load(f)
            if index is None:
                result = config
            else:
                index_list = index.split(delimiter)
                v = config
                for i in index_list:
                    v = v[i]
                result = v
            return from_dict(Config, result)

    @staticmethod
    def set_config(value, index: Optional[str] = None, delimiter: str = '.'):
        """
        data/config.json의 값을 가져온 후 index의 값을 value로 설정함.

        :param value: 설정할 값
        :param index: 접근할 인덱스
        :param delimiter: 인덱스를 나눌 구분자
        :raises KeyError: 인덱스를 찾을 수 없을 경우
        :raises dacite.WrongTypeError: 해당 설정 값의 타입이 올바르지 않을 경우
        :return:
        """
        index_list = index.split(delimiter)
        config_data = Config.get_config()
        temp = config_data
        for idx in index_list[:-1]:  # config_data의 참조인 상태를 유지하기 위해 [:-1]을 함
            temp = temp[idx]  # FIXME: TypeError: 'Config' object is not subscriptable
        temp[index_list[-1]] = value  # temp는 config_data의 참조이므로 config_data의 값이 변경됨
        with open("config.json", 'w') as f:
            json.dump(config_data, f)
