import re
from simulation.GameLogic.Particle.particle import Particle, ParticleDirections
from simulation.GameLogic.Particle.particle_utils import RemoveEntity, TryToMoveParticleDown


def Wood(movable_entites: list[Particle], particle_directions: ParticleDirections,entity: Particle) -> list[Particle]:
    movable_entites = TryToMoveParticleDown(movable_entites, particle_directions, entity)

    return movable_entites

def WoodBurned(movable_entites: list[Particle], entity: Particle) -> list[Particle]:
    movable_entites = RemoveEntity(movable_entites, entity)

    return movable_entites