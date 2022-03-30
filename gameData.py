from dataclasses import dataclass

from simulation.board import Boards

@dataclass
class GameData:
    game_rounds : int
    game_speed : int
    elements : Boards
    boards : Boards

@dataclass
class Cave:
    birth_rate : int
    death_rate : int
    change_of_surviving : int