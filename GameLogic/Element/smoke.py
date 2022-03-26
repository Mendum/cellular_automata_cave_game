from simulation.GameLogic.Element.element import Element
from simulation.GameLogic.Particle.particle import Particle, ParticleDirections
from simulation.GameLogic.Particle.particle_utils import RemoveEntity


def SmokeLight(movable_entites: list[Particle], entity: Particle) -> list[Particle]:
    movable_entites = RemoveEntity(movable_entites, entity)
    return movable_entites

def SmokeDark(movable_entites: list[Particle], entity: Particle) -> list[Particle]:
    movable_entites = RemoveEntity(movable_entites, entity)
    movable_entites.append(Particle(entity.x, entity.y, Element.smoke_light.value, -1))
    return movable_entites