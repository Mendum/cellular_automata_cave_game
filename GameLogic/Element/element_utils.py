import numpy as np
from GameLogic.Particle.particle import Particle
from GameLogic.Particle.particle_utils import GetParticleValue
from GameLogic.Element.element import IsWater, IsWood, IsWoodBurned, IsSand, IsFire, IsSmokeLight, IsSmokeDark
from simulation.GameLogic.Element.element import IsGrass
from simulation.GameLogic.Particle.particle_utils import GetParticleDirection

def GetAllMovableEntities(board: np.ndarray) -> list[Particle]:

    movable_entites = []
    
    for x, y in np.ndindex(board.shape):
        if IsMovable(board, x, y):
            movable_entites.append(Particle(x, y, GetParticleValue(board, x, y), -1))
    
    return movable_entites

def IsMovable(board: np.ndarray, x: int, y: int) -> bool:

    if IsWater(GetParticleValue(board, x, y)):
        return True
    if IsWood(GetParticleValue(board, x, y)):
        return True
    if IsWoodBurned(GetParticleValue(board, x, y)):
        return True
    if IsSand(GetParticleValue(board, x, y)):
        return True
    if IsFire(GetParticleValue(board, x, y)):
        return True
    if IsSmokeLight(GetParticleValue(board, x, y)):
        return True
    if IsSmokeDark(GetParticleValue(board, x, y)):
        return True
    if IsGrass(GetParticleValue(board, x, y)):
        return True
    
    return False