from pygame.font import FontType

from game.ui.base import FloatUIPosition, FloatUISize
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable
from game.ui.templates.slider import Scrollbar


class DropdownItem(Interactable):
    def __init__(self, pos: FloatUIPosition, size: FloatUISize):
        super().__init__(pos, size)


class Dropdown[T](Interactable):
    def __init__(self,
                 items: list[T],
                 default_idx: int,
                 font: FontType,
                 max_size: FloatUISize,
                 scrollbar: Scrollbar | None,
                 pos: FloatUIPosition,
                 size: FloatUISize,
                 background: RGB):
        """
        드롭다운 메뉴 객체를 생성함

        ``item_repr`` 메서드를 오버라이딩해 아이템들이 드롭다운 메뉴에서 표시되는 방법을 정의

        :param items: 아이템의 목록, 각 아이템은 __repr__ 특수 메서드를 구현한 상태여야 함
        :param default_idx: items에 접근할 인덱스, -1일 경우 아무것도 선택되지 않은 상태로 드롭다운 객체가 생성됨
        :param font: 드롭다운 목록에서 사용될 폰트
        :param max_size: 드롭다운 메뉴가 펼쳐질 때의 최대 크기
        :param scrollbar: 만약 ``None`` 일 경우 ``max_size`` 값은 무시되며 모든 값을 펼쳐서 보여줌
        :param pos: 드롭다운 메뉴의 위치
        :param size: 드롭다운 메뉴의 크기
        :param background: 드롭다운 메뉴의 배경색
        """
        super().__init__(pos, size)
        self.items = items
        self.current_idx = default_idx
        self.font = font
        self.max_size = max_size
        self.scrollbar = scrollbar
        self.pos = pos
        self.size = size
        self.background = background
        self.extended = False

    def item_repr(self, idx: T) -> str:
        if idx == -1:
            return "-"
        else:
            return self.items[idx].__repr__()

    def render(self):
        # TODO: 우측에 삼각형 아이콘을 배치해 만약 self.extended 가 true일 경우와 false일 경우를 알 수 있도록 만들기
        #       드롭다운 위치에 item_repr 사용해 현재 값 표시하기
        pass
