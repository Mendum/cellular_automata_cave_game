import numpy as np
from simulation.GameLogic.Element.water import TryToDisplacesWater
from simulation.GameLogic.Particle.particle import Particle, ParticleDirections
from simulation.GameLogic.Particle.particle_utils import TryToMoveParticleDiagonal, TryToMoveParticleDown


def Grass(movable_entites: list[Particle], particle_directions: ParticleDirections, board: np.ndarray, entity: Particle) -> list[Particle]:
    
    movable_entites = TryToMoveParticleDown(movable_entites, particle_directions, entity)
    movable_entites = TryToDisplacesWater(movable_entites, particle_directions, entity, board)
    
    return movable_entites