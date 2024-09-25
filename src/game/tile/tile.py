from game.tile.structure import *
from game.tile.types import *
from game.tile.base import *
from game.unit.unit import *

from utils.config import Config

from queue import PriorityQueue
import json


class CommonTile(BaseTile):       pass
class HillTile(CommonTile):       pass
class FieldTile(CommonTile):      pass
class MountainTile(CommonTile):   pass


class TileMap(BaseTileMap):
    @staticmethod
    def __parse_map(raw_map_data: list[str]) -> BaseTileMap:
        metadata = raw_map_data["metadata"]
        map_data = raw_map_data["map_data"]

        parsed_map: list[list[BaseTile]] = [ 
            [ CommonTile(i, j) for j in range(metadata["map_size"]) ] \
                for i in range(metadata["map_size"]) ]

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
                        tile.construct_structure(
                            SupplyBaseStructure(tile_mod["structure"]["faction"])) 
                    case "HQ":
                        tile.construct_structure(
                            HQStructure(tile_mod["structure"]["faction"]))
            except KeyError:
                pass

            try:
                match (tile_mod["unit"]):
                    case "ant":
                        tile.place_unit(Ant(x, y, tile_mod["unit"]["faction"], 
                                                  tile_mod["unit"]["hp"]))
                    case "stag_beetle":
                        tile.place_unit(StagBeetle(x, y, tile_mod["unit"]["faction"], 
                                                         tile_mod["unit"]["hp"]))
                    case "bombardier_beetle":
                        tile.place_unit(BombardierBeetle(x, y, tile_mod["unit"]["faction"], 
                                                               tile_mod["unit"]["hp"]))
                    case "aphid":
                        tile.place_unit(Aphid(x, y, tile_mod["unit"]["faction"], 
                                                    tile_mod["unit"]["hp"]))
            except KeyError:
                pass

        return parsed_map

    
    def __init__(self, map_name: str) -> None:
        with open(f"../assets/maps/{map_name}.json") as file_stream:
            raw_map_data: dict = json.loads(file_stream.read())

            self.tile_map: list[BaseTileMap] = self.__parse_map(raw_map_data)


class CommonTile(BaseTile):
    def __init__(self, q: int, r: int) -> None:
        super().__init__(q, r)

    def __repr__(self) -> str:
        return f"Tile({self.position.q}, {self.position.r})"

    def on_arrived(self) -> None:
        pass

    def get_neighbors(self, tile_map: TileMap) -> list[AxialCoordinates]:
        # TODO: 테스트 필요
        super().get_neighbors()
        return [ tile_map[self.position.q+v.value.q][self.position.r+v.value.r] \
                for v in HexDirectionVectors ]

    def get_path(self, destination: Position) -> list[Position]:
        # TODO: 테스트 필요
        frontier = PriorityQueue()
        frontier.put((self, 0))

        trail = {}
        far_cost = {}

        trail[self] = None
        far_cost[self] = 0

        while not frontier.empty():
            curr = frontier.get()

            if curr[0].position == destination:
                break

            for nxt in curr[0].get_neighbors():
                new_cost = far_cost[self] + self.get_distance(nxt)
                if nxt not in far_cost or new_cost < far_cost[self]:
                    far_cost[self] = new_cost
                    prior = new_cost + nxt.movement_cost
                    frontier.put(nxt, prior)
                    trail[nxt] = self


class HillTile(CommonTile):
    pass


class FieldTile(CommonTile):
    pass


class MountainTile(CommonTile):
    pass
