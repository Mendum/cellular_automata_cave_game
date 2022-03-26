import numpy as np
from simulation.GameLogic.Element.element import Element, IsRock

from simulation.GameLogic.Particle.particle import Particle
from simulation.GameLogic.Particle.particle_utils import GetParticleValue


def RenderNewBoard(boards: np.ndarray, calculated_movable_entites: list[Particle]) -> np.ndarray:

    for x, y in np.ndindex(boards.shape):
        if IsRock(GetParticleValue(boards, x, y)):
            boards[x, y] = Element.rock.value
        else:
            boards[x, y] = Element.air.value
    
    for movable_entity in calculated_movable_entites:
        boards[movable_entity.x, movable_entity.y] = movable_entity.value

    return boards