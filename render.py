import numpy as np
from simulation.GameLogic.Element.element import Element, IsRock
from simulation.GameLogic.Particle.particle import Particle
from simulation.GameLogic.Particle.particle_utils import GetParticleValue
from simulation.board import Boards


def RenderNewBoard(boards: Boards, calculated_movable_entites: list[Particle]) -> Boards:

    #game_board = boards.old_board
    for x, y in np.ndindex(boards.old_board.shape):
        if IsRock(GetParticleValue(boards.old_board, x, y)):
            boards.old_board[x, y] = Element.rock.value
        else:
            boards.old_board[x, y] = Element.air.value
    
    for movable_entity in calculated_movable_entites:
        boards.old_board[movable_entity.x, movable_entity.y] = movable_entity.value

    return boards