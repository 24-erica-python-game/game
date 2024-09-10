import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional


_config_path = "config.json"  # TODO: 경로를 지정해야 함.


class OnKeyErrorBehavior(Enum):
    ReturnNone = 0
    RaiseError = 1


@dataclass
class Font:
    default_font: str = "malgungothic"
    default_size: float = 18.0


@dataclass
class Config:
    font: Font

    @staticmethod
    def get_config(index: Optional[str] = None,
                   delimiter: str = '.',
                   on_key_error: OnKeyErrorBehavior = OnKeyErrorBehavior.ReturnNone):
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
        :param on_key_error: 인덱스를 찾을 수 없을 경우 처리할 행동
        :raises KeyError: 인덱스를 찾을 수 없으며 on_key_error가 RaiseError로 설정되어있을 경우
        :raises FileNotFoundError: 파일이 없는 경우
        :return: 찾은 결과, 만약 인덱스를 찾지 못했으며 on_key_error가 ReturnNone일 경우 None이 리턴됨
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
        data/config.json의 값을 가져온 후 index의 값을 value로 설정함.

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
        index_list = index.split(delimiter)
        config_data = Config.get_config(on_key_error=OnKeyErrorBehavior.RaiseError)
        temp = config_data
        for idx in index_list[:-1]:  # config_data의 참조인 상태를 유지하기 위해 [:-1]을 함
            temp = temp[idx]
        temp[index_list[-1]] = value  # temp는 config_data의 참조이므로 config_data의 값이 변경됨
        with open(_config_path, 'w') as f:
            json.dump(config_data, f)