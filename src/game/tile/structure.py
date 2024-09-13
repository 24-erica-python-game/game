from src.game.tile.base import BaseStructure, BaseTile


class HQStructure(BaseStructure):
    def on_arrived(self, base_tile: BaseTile) -> None:
        super().on_arrived(base_tile)


class SupplyBaseStructure(BaseStructure):
    def on_arrived(self, base_tile: BaseTile) -> None:
        super().on_arrived(base_tile)

        supply_reserve = base_tile.placed_unit.supply_reserve
        supply_reserve = (supply_reserve+100)%100
