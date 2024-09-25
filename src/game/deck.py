from enum import IntEnum
from typing import Optional

from src.game.unit.base import BaseUnit

type t_unit_data = list[BaseUnit, int]

class SetMode(IntEnum):
    ADD = 0
    SET = 1
    SUB = 2


class Deck[T]:
    def __init__(self):
        self.deck: dict[T, t_unit_data] = dict()

    def get_amount(self, key: T) -> int:
        """
        유닛의 수량을 구함, 만약 유닛이 덱에 존재하지 않을 경우 0을 반환함
        :param key: 덱에서 찾을 유닛의 키
        :return: 찾은 유닛의 수량
        """
        try:
            return self.deck[key][1]
        except KeyError:
            return 0

    def get_unit(self, key: T) -> Optional[BaseUnit]:
        """
        유닛 클래스를 구함, 만약 덱에 존재하지 않을 경우 None을 반환함
        :param key: 덱에서 찾을 유닛 클래스
        :return: 찾은 유닛 클래스
        """
        try:
            return self.deck[key][0]
        except KeyError:
            return None

    def set_amount(self, key: T, amount: int, mode: SetMode):
        """
        유닛의 수량을 정함.

        만약 mode가 다음과 같을 경우:

        - SetMode.ADD일 경우 현재 수량에 amount를 더함

        - SetMode.SET일 경우 현재 수량에 관계없이 amount 값으로 정해짐

        - SetMode.SUB일 경우 현재 수량에서 amount를 뺌

        수량을 계산한 후 현재 유닛 수량이 음수일 경우 0이 됨
        :param key: 접근할 키
        :param amount: 수량
        :param mode: 연산 모드
        :return:
        """
        match mode:
            case SetMode.ADD:
                self.deck[key][1] += amount
            case SetMode.SET:
                self.deck[key][1] = amount
            case SetMode.SUB:
                self.deck[key][1] -= amount

        if self.deck[key][1] < 0:
            self.deck[key][1] = 0

    def set_unit(self, key: T, unit: BaseUnit):
        """
        유닛을 수량이 0인 상태로 덱에 추가함.
        :param key: 접근할 키
        :param unit: 유닛 클래스
        :return:
        """
        u: t_unit_data = [unit, 0]
        self.deck[key] = u
