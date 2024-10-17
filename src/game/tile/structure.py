from game.tile.base import BaseStructure, BaseTile
from game.rule import GameSystem


class HQStructure(BaseStructure):
    def __init__(self, faction: int) -> None:
        super().__init__(faction)

    def on_arrived(self, base_tile: BaseTile) -> None:
        super().on_arrived(base_tile)

        if base_tile.placed_unit.faction != self.faction:
            GameSystem().players[self.faction].surrender()
            # GameSystem의 인스턴스를 만들고 플레이어를 패배시키는 것은
            # 의도된 대로 작동하지 않을 것이라고 확신함. GameSystem의 인스턴스를 만들어 패배시키지 말고
            # GameSystem의 인스턴스를 참조해 패배 메서드를 호출하는것이 맞다고 생각함.

class SupplyBaseStructure(BaseStructure):
    def __init__(self, faction: int) -> None:
        super().__init__(faction)

    def on_arrived(self, base_tile: BaseTile) -> None:
        super().on_arrived(base_tile)

        if base_tile.placed_unit.faction == self.faction:
            base_tile.placed_unit.supply_reserve = (base_tile.placed_unit.supply_reserve+100)%100
