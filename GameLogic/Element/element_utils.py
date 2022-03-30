from pprint import pprint
import numpy as np
from GameLogic.Particle.particle import Particle
from GameLogic.Particle.particle_utils import GetParticleValue
from simulation.GameLogic.Element.element import IsWater, LoadJsonFile
from simulation.GameLogic.Element.water import GetWaterFlowDirection
from simulation.board import Boards

def GetAllMovableEntities(boards: Boards) -> list[Particle]:

    movable_entites = []
    json_elements = LoadJsonFile()
    
    for x, y in np.ndindex(boards.old_board.shape):
        for element in json_elements:
            if element['value'] == GetParticleValue(boards.old_board, x, y):
                if IsMovable(element):
                    if IsWater(element['value']):
                        if boards.flow_direction_board[x, y] == 0:
                            flow_direction = -1
                        else:
                            flow_direction = boards.flow_direction_board[x, y]
                        movable_entites.append(Particle(x, y, element['value'], flow_direction))
                    else:
                        movable_entites.append(Particle(x, y, element['value'], 0))
    
    #pprint(movable_entites)
    return movable_entites

def IsMovable(element) -> bool:
    return element['movable']