from dataclasses import dataclass


@dataclass
class GameRule:
    map_size: tuple[int, int]  # 맵 크기
    enable_fow: bool           # 전장의 안개
    start_ticket: int          # 시작시 주어지는 티켓의 값
    end_ticket: int = 0        # 티켓이 이 이하로 떨어질 경우 종료되는 값
