import numpy as np
from numpy import random, ndarray
from nptyping import NDArray, Float64
from dataclasses import dataclass
import os
from simulation.GameLogic.Element.element import Element, IsRock
from simulation.GameLogic.Particle.particle import Particle
from simulation.GameLogic.Particle.particle_utils import GetParticleValue

@dataclass
class Boards:
    old_board : np.ndarray
    temp_board : np.ndarray

def generateBoard(change_of_surviving: float) -> np.ndarray:
    board = random.rand(100, 100).round(2)
    temp_map = np.zeros(board.shape, dtype=float)

    for x, y in np.ndindex(board.shape):
        if(board[x][y] > change_of_surviving):
            temp_map[x, y] = 1

    return temp_map

def GenerateTempBoard() -> np.ndarray:
    return np.zeros((100, 100))

def RenderNewBoard(boards: np.ndarray, calculated_movable_entites: list[Particle]) -> np.ndarray:

    for x, y in np.ndindex(boards.shape):
        if IsRock(GetParticleValue(boards, x, y)):
            boards[x, y] = Element.rock.value
        else:
            boards[x, y] = Element.air.value
    
    for movable_entity in calculated_movable_entites:
        boards[movable_entity.x, movable_entity.y] = movable_entity.value

    return boards

def saveToFile(map):
    np.savetxt('text.txt', map, fmt='%s')

def readFromFile():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'simulation/simulation/GameLogic/Board/board.txt')
    map = np.loadtxt('text.txt')
    #print(map)
    return map