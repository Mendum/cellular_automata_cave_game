from pprint import pprint
from simulation.GameLogic.Element.element import Element, IsFire, IsRock, IsSand, IsWater, IsWood
from simulation.GameLogic.Particle.particle import Particle, ParticleDirections
from simulation.GameLogic.Particle.particle_utils import GetParticleValue, RemoveEntity
from simulation.board import Boards

def CanFireSpread(particle_directions: ParticleDirections) -> bool:
    wood_is_below: bool = IsWood(particle_directions.vertical_down.value)

    return wood_is_below

def FireSpread(particle_directions: ParticleDirections) -> list[Particle]:

    fire_source = particle_directions.current
    spread_left = particle_directions.diagonal_down_left
    spread_right = particle_directions.diagonal_down_right
    wood_is_on_left = IsWood(spread_left.value)
    wood_is_on_right = IsWood(spread_right.value)

    if wood_is_on_left and wood_is_on_right:
        return [
            Particle(fire_source.x, fire_source.y+1, Element.fire.value, 0),
            Particle(fire_source.x, fire_source.y-1, Element.fire.value, 0)
            ]

    elif wood_is_on_left:
        return [ Particle(fire_source.x, fire_source.y-1, Element.fire.value, 0)]

    elif wood_is_on_right:
        return [Particle(fire_source.x, fire_source.y+1, Element.fire.value, 0)]

    return []

def TryToSpreadFire(movable_entites: list[Particle], particle_directions: ParticleDirections, boards: Boards) -> list[Particle]:
    entity = particle_directions.current
    if CanFireSpread(particle_directions):
        movable_entites = RemoveEntity(movable_entites, entity)
        movable_entites = RemoveEntity(movable_entites, particle_directions.vertical_down)
        #temp_movable_entites = FireSpread(particle_directions)
        temp_temp = FireSpread(particle_directions)
        movable_entites.extend(temp_temp)
        movable_entites.append(Particle(entity.x, entity.y, Element.smoke_dark.value, 0))
        movable_entites.append(Particle(entity.x+1, entity.y, Element.wood_burned.value, 0))
    
    return movable_entites

def CanFireBeExtinguish(particle_directions: ParticleDirections) -> bool:
    rock_is_below: bool = IsRock(particle_directions.vertical_down.value)
    water_is_below: bool = IsWater(particle_directions.vertical_down.value)
    sand_is_below: bool = IsSand(particle_directions.vertical_down.value)
    print(f'rock_is_below', rock_is_below)
    print(f'water_is_below', water_is_below)
    print(f'sand_is_below', sand_is_below)

    return (rock_is_below or water_is_below or sand_is_below)

def FireExtinguish(movable_entites: list[Particle], particle_directions: ParticleDirections, boards: Boards) -> list[Particle]:

    def GenerateSmokeParticle(particle: Particle) -> bool:
        return (particle_directions.current.x == particle.x and particle_directions.current.y == particle.y)

    def ChangeEntitesValue(particle: Particle):
        print('curi')
        particle_value = GetParticleValue(boards.old_board, particle_directions.vertical_down.x, particle_directions.vertical_down.y)
        if GenerateSmokeParticle(particle):
            print('muri')
            if IsRock(particle_value) or IsWater(particle_value) or IsSand(particle_value) or IsFire(particle_value):
                print('v afriki')
                return Particle(particle.x, particle.y, Element.smoke_light.value, 0)
            else:
                return particle
        else:
            return particle

    return list(map(ChangeEntitesValue, movable_entites))

def TryToExtinguishFire(movable_entites: list[Particle], particle_directions: ParticleDirections, boards: Boards ) -> list[Particle]:
    entity = particle_directions.current
    if CanFireBeExtinguish(particle_directions):
        print('filip')
        temp_temp = FireExtinguish(movable_entites, particle_directions, boards)
        movable_entites = RemoveEntity(movable_entites, entity)
        movable_entites.extend(temp_temp)
    
    pprint(movable_entites)
    return movable_entites