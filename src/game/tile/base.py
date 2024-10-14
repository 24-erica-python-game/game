from queue import PriorityQueue
from abc import ABCMeta, abstractmethod
from typing import Any, Optional, TYPE_CHECKING

from game.rule import GameSystem
from src.game.unit.base import BaseUnit
from src.game.tile.types import *

if TYPE_CHECKING:
    from . import BaseTile


class BaseStructure(metaclass=ABCMeta):
    def __init__(self, faction: int) -> None:
        self.faction = faction

    @abstractmethod
    def on_arrived(self, base_tile: BaseTile) -> None:
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
        if self.placed_structure is not None:
            self.placed_structure.on_arrived(self)

    def place_unit(self, unit: BaseUnit) -> None:
        self.placed_unit = unit

    def place_structure(self, structure: BaseStructure) -> None:
        self.placed_structure = structure

    def get_neighbors(self) -> list[BaseTile]:
        map_data = GameSystem().map_data

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
        a -> b로 이동하는 경로 리스트 반환, 없을 경우 `None` 반환
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
