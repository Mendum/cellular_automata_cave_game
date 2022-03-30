from simulation.GameLogic.Element.element import Element
from simulation.GameLogic.Particle.particle import Particle, ParticleDirections
from simulation.GameLogic.Particle.particle_utils import RemoveEntity
from simulation.board import Boards

def TryToSmokeLight(movable_entites: list[Particle], particle_directions: ParticleDirections, boards: Boards) -> list[Particle]:
    entity = particle_directions.current
    return RemoveEntity(movable_entites, entity)

def TryToSmokeDark(movable_entites: list[Particle], particle_directions: ParticleDirections, boards: Boards) -> list[Particle]:
    entity = particle_directions.current
    movable_entites = RemoveEntity(movable_entites, entity)
    movable_entites.append(Particle(entity.x, entity.y, Element.smoke_light.value, 0))
    return movable_entites