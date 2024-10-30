from game.tile.base import BaseStructure, BaseTile
from game.rule import GameSystem


class HQStructure(BaseStructure):
    def __init__(self, faction: int, parent_tile: 'BaseTile') -> None:
        super().__init__(faction, parent_tile)

    def on_unit_arrived(self) -> None:
        super().on_unit_arrived()

        if self.parent_tile.placed_unit.faction != self.faction:
            game_sys = GameSystem()
            game_sys.defeat_player(game_sys.players[self.faction])

class SupplyBaseStructure(BaseStructure):
    def __init__(self, faction: int, parent_tile: 'BaseTile') -> None:
        super().__init__(faction, parent_tile)

    def on_unit_arrived(self) -> None:
        super().on_unit_arrived()

        placed_unit = self.parent_tile.placed_unit

        if placed_unit.faction == self.faction:
            self.parent_tile.placed_unit.supply_reserve = (placed_unit.supply_reserve + 100) % 100
