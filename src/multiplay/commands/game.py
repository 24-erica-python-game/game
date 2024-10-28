from src.game.rule import GameSystem
from src.game.command import register

@register
def set_map(map_name: str):
    from src.game.tile.tile import MapManager
    from src.game.tile.base import BaseTile

    try:
        tile_map: list[list[BaseTile]] = MapManager(map_name).map_data

        GameSystem().set_map(tile_map)
        print(f"Map: {map_name}")
    except FileNotFoundError:
        print(f"Map: {map_name} not found.")

@register
def set_rule(map_size: tuple[int, int], enable_fow: bool, start_ticket: int):
    from src.game.rule import GameRule

    GameSystem(GameRule(
        map_size=map_size,
        enable_fow=enable_fow,
        start_ticket=start_ticket,
    ))
    print(f"Ruleset: Map size: {map_size[0]}x{map_size[1]} \n"
          f"         FoW: {enable_fow} \n" 
          f"         Ticket: {start_ticket} \n")
