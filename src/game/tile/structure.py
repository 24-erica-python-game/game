from game.tile.base import BaseStructure, BaseTile
from game.rule import GameSystem


class HQStructure(BaseStructure):
    def __init__(self, faction: int) -> None:
        super().__init__(faction)

    def on_arrived(self, base_tile: BaseTile) -> None:
        super().on_arrived(base_tile)

        if base_tile.placed_unit.faction != self.faction:
            GameSystem().players[self.faction].surrender()

class SupplyBaseStructure(BaseStructure):
    def __init__(self, faction: int) -> None:
        super().__init__(faction)

    def on_arrived(self, base_tile: BaseTile) -> None:
        super().on_arrived(base_tile)

        if base_tile.placed_unit.faction == self.faction:
            base_tile.placed_unit.supply_reserve = (base_tile.placed_unit.supply_reserve+100)%100
