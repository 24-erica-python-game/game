from typing import Literal, TypeVar

from pygame import gfxdraw as gfx
from pygame.font import FontType

from game.ui.base import UIPosition, UISize, UIAlignment
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable
from game.ui.templates.textbox import TextBox

t_button_id = TypeVar('t_button_id')


class RadioButtonGroup:
    def __init__(self,
                 font: FontType,
                 label_pos: Literal[UIAlignment.left, UIAlignment.right],
                 label_alignment: Literal[UIAlignment.left, UIAlignment.center, UIAlignment.right, "test"],
                 label_color: RGB,
                 label_distance: int,
                 default_active_id: t_button_id,
                 button_color: RGB,
                 active_color: RGB):
        """
        라디오버튼 그룹을 생성함. 그룹당 하나의 활성화된 라디오버튼만 존재할 수 있음.
        :param font: 라디오버튼 레이블의 폰트
        :param label_pos: 라디오버튼 레이블의 위치
        :param label_alignment: 라디오버튼 레이블의 정렬 위치
        :param label_color: 라디오버튼 레이블의 색상
        :param label_distance: 라디오버튼 레이블이 버튼과 떨어져 있는 간격
        :param default_active_id: 처음 상태에서 활성화될 버튼의 ID
        :param button_color: 버튼의 기본 색상
        :param active_color: 활성화 되었을 경우 버튼의 색상
        """
        self.buttons = []
        self.font = font
        self.label_pos = label_pos
        self.label_alignment = label_alignment
        self.label_color = label_color
        self.label_distance = label_distance
        self.active_id = default_active_id
        self.button_color = button_color
        self.active_color = active_color

    def check_buttons_clicked(self):
        """
        라디오버튼 그룹의 버튼이 클릭되었는지를 체크하는 함수
        :return:
        """
        for button in self.buttons:
            button.check_button_clicked()

    def update_buttons(self):
        """
        라디오버튼 그룹의 버튼을 모두 업데이트함.
        :return:
        """
        for button in self.buttons:
            button.update()

    def set_active(self, active_id: t_button_id):
        """
        라디오버튼을 활성화한 상태로 설정함.
        :param active_id: 활성화할 버튼의 ID
        :return:
        """
        self.active_id = active_id

    def get_current_active(self) -> t_button_id:
        """
        현재 활성화된 버튼의 ID를 반환함.
        :return:
        """
        return self.active_id

    def get_longest_text_size(self) -> UISize:
        """
        라디오버튼 그룹 내의 버튼의 레이블중 가장 긴 길이를 반환함.
        :return:
        """
        longest = max([self.font.render(button.label, True, self.label_color).get_size()
                       for button in self.buttons])
        return UISize(longest[0], longest[1])


class RadioButton(Interactable):
    def __init__(self,
                 group: RadioButtonGroup,
                 label: str,
                 pos: UIPosition,
                 radius: float,
                 button_id: t_button_id):
        """
        라디오버튼 템플릿. 라디오버튼은 라디오버튼 그룹에 속해있어야 함.
        :param group: 버튼이 속해있는 그룹
        :param label: 라디오버튼의 레이블
        :param pos: 버튼의 위치
        :param radius: 버튼의 반지름
        :param button_id: 버튼의 ID
        """
        super().__init__(UIPosition(pos.x - radius, pos.y - radius),
                         UISize(radius * 2, radius * 2))
        self.group = group
        self.label = label
        self.pos = pos
        self.radius = radius
        self.button_id = button_id

        self.tst_pos = UIPosition(pos.x - radius, pos.y - radius)
        self.tst_size = UISize(radius * 2, radius * 2)

        group.buttons.append(self)

    def check_button_clicked(self):
        """
        버튼이 클릭되었는지 체크함.
        :return:
        """
        if self.is_mouse_in_area() and pg.mouse.get_pressed()[0]:
            self.group.set_active(self.button_id)

    def update(self):
        display = pg.display.get_surface()
        pos = self.pos
        gfx.aacircle(display,
                     pos.x,
                     pos.y,
                     int(max(self.radius, 2)),
                     self.group.button_color)

        label = self.group.font.render(self.label, True, self.group.label_color)
        longest_text_size = self.group.get_longest_text_size()
        text_size = UISize(label.get_size()[0], label.get_size()[1])
        textbox_pos_x = 0

        match self.group.label_pos:
            case UIAlignment.left:
                textbox_pos_x = pos.x - self.group.label_distance - longest_text_size.x
            case UIAlignment.right:
                textbox_pos_x = pos.x + self.group.label_distance

        textbox = TextBox(UIPosition(textbox_pos_x, pos.y - text_size.y / 2),
                          longest_text_size,
                          self.group.font,
                          self.label)

        textbox.update()

        if self.group.active_id == self.button_id:
            gfx.aacircle(display,
                         pos.x,
                         pos.y,
                         int(max(self.radius, 2)) - 2,
                         self.group.active_color)
            gfx.filled_circle(display,
                         pos.x,
                         pos.y,
                         int(max(self.radius, 2)) - 2,
                         self.group.active_color)


if __name__ == "__main__":
    import pygame as pg

    from game.ui.color import Color

    pg.init()

    small_font = pg.font.SysFont("malgungothic", 14, False, False)

    # 화면 크기 지정
    size = (1280, 600)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Buggy Buddies")

    # FPS 관련 설정
    running = True
    clock = pg.time.Clock()

    radio_group = RadioButtonGroup(font=small_font,
                                   label_pos=UIAlignment.right,
                                   label_alignment=UIAlignment.center,
                                   label_color=RGB(0, 0, 0),
                                   label_distance=20,
                                   default_active_id='radio_button_1',
                                   button_color=RGB(77, 77, 77),
                                   active_color=RGB(35, 188, 35))
    radio_button_1 = RadioButton(radio_group, "테스트", UIPosition(500, 100), 6.5, 'radio_button_1')
    radio_button_2 = RadioButton(radio_group, "label_pos와 label_alignment 값을 변경해", UIPosition(500, 120), 6.5,
                                 'radio_button_2')
    radio_button_3 = RadioButton(radio_group, "레이블 위치를 변경 가능하다", UIPosition(500, 140), 6.5, 'radio_button_3')

    while running:
        screen.fill(Color.WHITE)
        clock.tick(30)

        radio_group.check_buttons_clicked()
        radio_group.update_buttons()

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False

        pg.display.flip()
