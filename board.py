import numpy as np
from numpy import random, ndarray
from nptyping import NDArray, Float64
from dataclasses import dataclass
import os

@dataclass
class Boards:
    old_board : np.ndarray
    flow_direction_board : np.ndarray

def generateBoard(change_of_surviving: float) -> np.ndarray:
    board = random.rand(100, 100).round(2)
    temp_map = np.zeros(board.shape, dtype=float)

    for x, y in np.ndindex(board.shape):
        if(board[x][y] > change_of_surviving):
            temp_map[x, y] = 1

    return temp_map

def GenerateTempBoard() -> np.ndarray:
    return np.zeros((100, 100))

def GenerateFlowDirectionBoard() -> np.ndarray:
    return np.full_like(GenerateTempBoard(), -1, dtype=np.double)

def saveToFile(map):
    np.savetxt('text.txt', map, fmt='%s')

def readFromFile():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'simulation/simulation/GameLogic/Board/board.txt')
    map = np.loadtxt('text.txt')
    #print(map)
    return map