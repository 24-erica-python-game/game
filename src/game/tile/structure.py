from game.tile.base import BaseStructure, BaseTile
from game.rule import GameSystem


class HQStructure(BaseStructure):
    def __init__(self, faction: int, parent_tile: type['BaseTile']) -> None:
        super().__init__(faction, parent_tile)

    def on_unit_arrived(self) -> None:
        super().on_arrived()

        if self.parent_tile.placed_unit.faction != self.faction:
            GameSystem().players[self.faction].surrender()

class SupplyBaseStructure(BaseStructure):
    def __init__(self, faction: int, parent_tile: type['BaseTile']) -> None:
        super().__init__(faction, parent_tile)

    def on_unit_arrived(self) -> None:
        super().on_arrived()

        if self.parent_tile.placed_unit.faction == self.faction:
            self.parent_tile.placed_unit.supply_reserve = (self.parent_tile.placed_unit.supply_reserve+100)%100
