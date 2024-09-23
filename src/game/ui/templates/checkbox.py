from typing import Literal

from pygame.font import FontType

from game.ui.base import FloatUIPosition, FloatUISize
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable


class CheckBox(Interactable):
    def __init__(self,
                 font: FontType,
                 label: str,
                 active_color: RGB,
                 active_indicator_type: Literal["square", "check", "cross"],
                 pos: FloatUIPosition,
                 size: FloatUISize):
        super().__init__(pos, size)
