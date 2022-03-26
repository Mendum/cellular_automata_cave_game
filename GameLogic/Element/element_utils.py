import numpy as np
from GameLogic.Particle.particle import Particle
from GameLogic.Particle.particle_utils import GetParticleValue
from simulation.GameLogic.Element.element import LoadJsonFile

def GetAllMovableEntities(board: np.ndarray) -> list[Particle]:

    movable_entites = []
    json_elements = LoadJsonFile()
    
    for x, y in np.ndindex(board.shape):
        for element in json_elements:
            if element['value'] == GetParticleValue(board, x, y):
                if IsMovable(element):
                    movable_entites.append(Particle(x, y, element['value'], -1))
    
    return movable_entites

def IsMovable(element) -> bool:
    return element['movable']