from abc import ABCMeta, abstractmethod
from queue import PriorityQueue
from typing import Any

from game.rule import GameSystem
from src.game.tile.types import *
from src.game.unit.base import BaseUnit


# BaseStructure는 BaseTile을 참조하고, BaseTile은 BaseStructure를 참조하고 있음.
# BaseStructure를 2개 클래스에서 상속받고 있음.
# 이를 나타내면 아래와 같이 나타낼 수 있음.
#    ↙  HQ   ↖
#   ↓          BaseStructure ↔ BaseTile
#   ↓ Supply ↙                    ↓
#   ↓   ↓                         ↓
#          GameSystem

# 문제점은 BaseStructure와 BaseTile이 서로를 참조하고 있다는 것이다.
# 또한 GameSystem의 메서드를 호출할 때 GameSystem의 인스턴스를 새로 만들어서 메서드를 호출하는데
# 이는 의도된 대로 작동하지 않을 것이다. 새로 만들어져 초기화된 GameSystem은 현재 게임의 진행 상황을 반영하지 않고 있다.
# GameSystem의 인스턴스가 단 하나만 존재하고, GameSystem의 인스턴스의 메서드를 호출하는 방향으로 코드를 작성하는것이
# 의도된 대로 코드를 작동시킬 수 있다고 생각한다.
# 또는, 이벤트를 사용해서 GameSystem의 인스턴스가 이벤트를 수신받아, 해당 이벤트에 맞는 메서드를 GameSystem의 인스턴스가
# 적절히 처리하는 방법으로도 해결할 수 있다고 생각한다.

# 아래와 같은 구조로 수정하길 원함.
#  ↙  HQ   ↖
# ↓          BaseStructure ← BaseTile
# ↓ Supply ↙                    ↓
# ↓   ↓                         ↓
#          GameSystem (단 하나의 인스턴스만 존재하며 참조할 때 이 인스턴스를 참조해야 한다.)

# 또는

# 아래와 같은 구조로 수정하길 원함.
#  ↙  HQ   ↖
# ↓          BaseStructure ← BaseTile
# ↓ Supply ↙                    ↓
##################이벤트######################
# ↓   ↓                         ↓
#          GameSystem (단 하나의 인스턴스만 존재하며 참조할 때 이 인스턴스를 참조해야 한다.)

# 코드를 작성할 때 각 객체가 서로에게 의존하지 않도록 코드를 작성하면 좋겠음.

class BaseStructure(metaclass=ABCMeta):
    def __init__(self, faction: int) -> None:
        self.faction = faction

    @abstractmethod
    def on_arrived(self, base_tile: BaseTile) -> Any:
        """
        유닛이 도착했을 때 호출되어야 하는 메서드

        :param base_tile:
        :return: 상속된 구조물 클래스에서 구현한 메서드의 반환값
        """
        pass


class BaseTile(metaclass=ABCMeta):
    """
    https://www.redblobgames.com/grids/hexagons/
    기본: `Axial Coordinates` 사용,
    필요 시 `Cube Coordinates` 사용
    """

    @property
    def placed_unit(self) -> Optional[BaseUnit]:
        return self.placed_unit

    @property
    def placed_structure(self) -> Optional[BaseStructure]:
        return self.placed_structure

    def __init__(self, q: int, r: int,
                 defence_bonus: int = 0,
                 movement_cost: int = 1) -> None:
        self.position = Position(q, r)
        self.defence_bonus = defence_bonus
        self.movement_cost = movement_cost

    @placed_unit.setter
    def placed_unit(self, unit: BaseUnit) -> None:
        self.placed_unit = unit

    @placed_structure.setter
    def placed_structure(self, structure: BaseStructure) -> None:
        self.placed_structure = structure

    def on_unit_arrived(self) -> Any:
        """
        유닛이 도착했을 때 유닛은 현재 타일의 이 메서드를 호출해야 함.

        구조물이 있는 경우 구조물의 `on_arrived()` 메서드를 호출하게 됨, \n
        따라서 상속된 타일 클래스에서 구조물의 `on_arrived()` 메서드를 호출하는 대신 `super().on_unit_arrived()` 구문을 추가하면 됨.

        :return: 상속된 타일 클래스에서 구현한 메서드의 반환값
        """
        if self.placed_structure is not None:
            return self.placed_structure.on_arrived(self)

    def place_unit(self, unit: BaseUnit) -> None:
        """
        타일에 유닛을 배치함
        :param unit:
        :return:
        """
        self.placed_unit = unit

    def place_structure(self, structure: BaseStructure) -> None:
        """
        타일에 구조물을 배치함
        :param structure:
        :return:
        """
        self.placed_structure = structure

    def get_neighbors(self) -> list[Self]:
        """
        현재 타일의 이웃 타일 리스트 반환
        :return: 유효한 이웃 타일 리스트
        """
        map_data = GameSystem().map_data
        # FIXME: GameSystem의 인스턴스를 새로 만들고, 그 필드를 참조하기 때문에
        #        메모리 낭비의 우려가 있으며 의도된대로 작동하지 않을 수 있다고 생각함.

        def is_valid_position(p: Position) -> bool:
            q_size, r_size = GameSystem().ruleset.map_size
            return 0 <= p.q < q_size and 0 <= p.r < r_size

        return [
            map_data[self.position.q + v.value.q][self.position.r + v.value.r] \
            for v in HexDirectionVectors
            if is_valid_position(
                map_data[self.position.q + v.value.q][self.position.r + v.value.r].position
            )
        ]

    def get_path(self, b: Position) -> Optional[list[Position]]:
        """
        A 타일에서 B 타일로 이동하는 경로의 리스트 반환, 없을 경우 `None` 반환
        """

        # 경로 탐색 구현
        # TileMeta.get_path() 에서 경로 계산 결과 반환
        # UnitMeta.move() 에서 결과 값을 토대로 이동

        def g(t: BaseTile) -> float:
            # actual cost
            return float(t.movement_cost)

        def h(t: BaseTile) -> float:
            # heuristic func
            return t.position.distance_to(b)

        queue = PriorityQueue()
        queue.put((0, self.position, [self.position]))
        visited = set()

        while not queue.empty():
            _node = queue.get()

            current_cost: float = _node[0]
            current_position: Position = _node[1]
            path: list[Position] = _node[2]

            if current_position in visited:
                continue

            visited.add(current_position)

            if current_position == b:
                return path

            for neighbor in self.get_neighbors():
                if neighbor.position not in visited:
                    total_cost = current_cost + g(neighbor) + h(neighbor)
                    queue.put((total_cost, neighbor.position, path + [neighbor.position]))

        return None
