import json

from game.tile.structure import *
from game.unit.unit import *
from src.game.tile.base import *


class HillTile(BaseTile):
    def __init__(self, q: int, r: int) -> None:
        super().__init__(q, r, movement_cost=2, defence_bonus=1)

    def __repr__(self) -> str:
        return f"Tile({self.position.q}, {self.position.r})"

    def on_unit_arrived(self) -> None:
        pass


class FieldTile(BaseTile):
    def __init__(self, q: int, r: int) -> None:
        super().__init__(q, r, movement_cost=1, defence_bonus=0)

    def __repr__(self) -> str:
        return f"Tile({self.position.q}, {self.position.r})"

    def on_unit_arrived(self) -> None:
        pass


class MountainTile(BaseTile):
    def __init__(self, q: int, r: int) -> None:
        super().__init__(q, r, movement_cost=4, defence_bonus=3)

    def __repr__(self) -> str:
        return f"Tile({self.position.q}, {self.position.r})"

    def on_unit_arrived(self) -> None:
        pass


class TileMap:
    @staticmethod
    def __parse_map(raw_map_data: dict[str, Any]) -> list[list[BaseTile]]:
        metadata = raw_map_data["metadata"]
        map_data = raw_map_data["map_data"]

        parsed_map: list[list[BaseTile]] = [
            [FieldTile(i, j) for j in range(metadata["map_size"])] \
            for i in range(metadata["map_size"])]

        for tile_mod in map_data:
            if tile_mod["position"][0] >= metadata["map_size"] or \
                    tile_mod["position"][1] >= metadata["map_size"]:
                continue

            x: int = tile_mod["position"][0]
            y: int = tile_mod["position"][1]

            tile = parsed_map[y][x]

            try:
                match (tile_mod["tile"]):
                    case "hill":
                        parsed_map[y][x] = HillTile(x, y)
                        tile = parsed_map[y][x]
                    case "mountain":
                        parsed_map[y][x] = MountainTile(x, y)
                        tile = parsed_map[y][x]
            except KeyError:
                pass

            try:
                match (tile_mod["structure"]):
                    case "supply_base":
                        tile.place_structure(
                            SupplyBaseStructure(tile_mod["structure"]["faction"]))
                    case "HQ":
                        tile.place_structure(
                            HQStructure(tile_mod["structure"]["faction"]))
            except KeyError:
                pass

            try:
                match (tile_mod["unit"]):
                    case "ant":
                        tile.place_unit(
                            Ant(x, y,
                                tile_mod["unit"]["faction"],
                                tile_mod["unit"]["hp"], 0))
                    case "stag_beetle":
                        tile.place_unit(
                            StagBeetle(x, y,
                                       tile_mod["unit"]["faction"],
                                       tile_mod["unit"]["hp"], 0))
                    case "bombardier_beetle":
                        tile.place_unit(
                            BombardierBeetle(x, y,
                                             tile_mod["unit"]["faction"],
                                             tile_mod["unit"]["hp"], 0))
                    case "aphid":
                        tile.place_unit(
                            Aphid(x, y,
                                  tile_mod["unit"]["faction"],
                                  tile_mod["unit"]["hp"], 0))
            except KeyError:
                pass

        return parsed_map

    def __init__(self, map_name: str) -> None:
        with open(f"../assets/maps/{map_name}.json") as file_stream:
            raw_map_data: dict = json.loads(file_stream.read())

            self.tile_map: list[list[BaseTile]] = self.__parse_map(raw_map_data)
