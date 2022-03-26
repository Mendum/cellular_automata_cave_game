from calendar import month_abbr
from pprint import pprint
from re import I
from xml.dom.minidom import Entity
import numpy as np
from simulation.GameLogic.Element.element import Element, IsAir, IsRock, IsWater, IsWood
from simulation.GameLogic.Particle.particle import Particle, ParticleDirections
from simulation.GameLogic.Particle.particle_utils import IsParticleFalling, ParticleCanMoveHorizontalIntoAir, ParticleCanMoveHorizontalIntoWater, RemoveEntity, TryToMoveParticleDown
from simulation.board import Boards

def Water(movable_entites: list[Particle], particle_directions: ParticleDirections, board: np.ndarray, entity: Particle) -> list[Particle]:
    
    movable_entites = TryToMoveParticleDown(movable_entites, particle_directions, entity)
    movable_entites = TryToCombineWater(movable_entites, particle_directions, entity, board)
    movable_entites = TryToOverflowWater(movable_entites, particle_directions, entity)
    movable_entites = TryToDisplacesWood(movable_entites, particle_directions, entity, board)
    movable_entites = TryToSpillWaterIntoAir(movable_entites, particle_directions, entity, board)
    movable_entites = TryToSpillWaterIntoWater(movable_entites, particle_directions, entity, board)
    
    return movable_entites

def CanDisplacesWater(particle_directions: ParticleDirections) -> bool:
    water_can_be_displaced: bool = IsWater(particle_directions.vertical_down.value)

    return water_can_be_displaced

def CanDisplacesWood(particle_directions: ParticleDirections) -> bool:
    wood_can_be_displaced: bool = IsWood(particle_directions.vertical_down.value)

    return wood_can_be_displaced

def TryToOverflowWater(movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle) -> list[Particle]:
    if CanWaterOverflow(particle_directions):
        print('naredim novo vodo')
        movable_entites.append(Particle(entity.x-1, entity.y, Element.water.value, -1))
    
    return movable_entites

def TryToCombineWater(movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle, board: Boards) -> list[Particle]:
    if CanWaterCombine(particle_directions) and not IsParticleFalling(board, entity):
        movable_entites = RemoveEntity(movable_entites, entity)
        movable_entites.append(Particle(entity.x+1, entity.y, particle_directions.vertical_down.value + 1, -1))
    
    return movable_entites

#movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle
def TryToDisplacesWater(movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle, board: Boards) -> list[Particle]:
    if CanDisplacesWater(particle_directions) and not IsParticleFalling(board, entity):
        movable_entites = RemoveEntity(movable_entites, entity)
        movable_entites.append(Particle(entity.x, entity.y, particle_directions.vertical_down.value, -1))
        movable_entites.append(Particle(entity.x+1, entity.y, entity.value, -1))
    
    return movable_entites

def TryToDisplacesWood(movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle, board: Boards) -> list[Particle]:
    if CanDisplacesWood(particle_directions) and not IsParticleFalling(board, entity):
        movable_entites = RemoveEntity(movable_entites, entity)
        movable_entites.append(Particle(entity.x, entity.y, particle_directions.vertical_down.value, -1))
        movable_entites.append(Particle(entity.x+1, entity.y, entity.value, -1))

    return movable_entites

def TryToSpillWaterIntoAir(movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle, board: Boards) -> list[Particle]:
    if CanWaterSpill(particle_directions) and ParticleCanMoveHorizontalIntoAir(particle_directions) and not IsParticleFalling(board, entity):
        test = entity
        #pprint(movable_entites)
        temp_temp = WaterSpillIntoAir(particle_directions)
        movable_entites.extend(temp_temp)
        movable_entites = RemoveEntity(movable_entites, entity)
        movable_entites.append(Particle(test.x, test.y, (test.value - 1), test.flow_direction))
        pprint('to vrnem')
        pprint('====================')
        pprint(movable_entites)
    
    return movable_entites

def TryToSpillWaterIntoWater(movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle, board: Boards) -> list[Particle]:
    if CanWaterSpill(particle_directions) and ParticleCanMoveHorizontalIntoWater(particle_directions) and not IsParticleFalling(board, entity):
        test = entity

        pprint(f'1 :')
        pprint(movable_entites)
        temp_temp = WaterSpillIntoWater(particle_directions)
        movable_entites.extend(temp_temp)

        pprint(f'2 :')
        pprint(movable_entites)
        movable_entites = RemoveEntity(movable_entites, entity)
        movable_entites.append(Particle(test.x, test.y, (test.value - 1), test.flow_direction))
    
        pprint(f'3 :')
        pprint(movable_entites)

    return movable_entites

def CanWaterSpill(particle_directions: ParticleDirections) -> bool:
    water_can_spill: bool = particle_directions.current.value > 20
    is_rock_below: bool = IsRock(particle_directions.vertical_down.value)
    
    return water_can_spill and is_rock_below

def WaterSpillIntoAir(particle_directions: ParticleDirections) -> list[Particle]:
    water_level: float = GetWaterLevel(particle_directions.current.value)
    spill_curr: Particle = particle_directions.current

    can_go_left: bool = IsAir(particle_directions.horizontal_left.value)
    spill_left: Particle = particle_directions.horizontal_left

    can_go_right: bool = IsAir(particle_directions.horizontal_right.value)
    spill_right: Particle = particle_directions.horizontal_right

    water_flow_direction: int = GetWaterFlowDirection(particle_directions.current)
    #print('jaz sem')
    #print(particle_directions.current)
    #print('grem po zraku')
    #print(water_flow_direction)
    float_none: bool = water_flow_direction == -1
    float_in_left: bool = water_flow_direction == 1
    float_in_right: bool = water_flow_direction == 2

    #print(particle_directions.current)
    #print(float_none)
    #print(float_in_left)
    #print(float_in_right)
    #print(particle_directions.current)

    if water_level > 0:
        # hmmmmmm
        if can_go_left and can_go_right and float_none:
            print('grem v obe smeri')
            return [
                Particle(spill_left.x, spill_left.y, (spill_curr.value - 1), 1),
                Particle(spill_right.x, spill_right.y, (spill_curr.value - 1), 2)
            ]

        elif can_go_left and float_in_left:
            print('morem it levo')
            return [
                Particle(spill_curr.x, spill_curr.y, (spill_curr.value - 1), -1),
                Particle(spill_left.x, spill_left.y, (spill_curr.value - 1), 1)
            ]

        elif can_go_right and float_in_right:
            print('morem it desno')
            return [
                Particle(spill_curr.x, spill_curr.y, (spill_curr.value - 1), -1),
                Particle(spill_right.x, spill_right.y, (spill_curr.value - 1), 2)
            ]

    return []

def WaterSpillIntoWater(particle_directions: ParticleDirections) -> list[Particle]:
    water_level: float = GetWaterLevel(particle_directions.current.value)
    spill_curr: Particle = particle_directions.current

    spill_left: Particle = particle_directions.horizontal_left
    can_combine_left: bool = IsWater(particle_directions.horizontal_left.value)

    spill_right: Particle = particle_directions.horizontal_right
    can_combine_right: bool = IsWater(particle_directions.horizontal_right.value)

    water_flow_direction: int = GetWaterFlowDirection(particle_directions.current)
    float_none: bool = water_flow_direction == -1
    float_in_left: bool = water_flow_direction == 1
    float_in_right: bool = water_flow_direction == 2

    print('bol je tu problem')

    if water_level > 0:
        if can_combine_left and can_combine_right and float_none:
            return [
                Particle(spill_left.x, spill_left.y, (spill_left.value + 1), 1),
                Particle(spill_right.x, spill_right.y, (spill_right.value + 1), 2)
            ]
        
        elif can_combine_left and (float_in_left or float_none):
            return [
                Particle(spill_left.x, spill_left.y, (spill_left.value + 1), 1)
            ]

        elif can_combine_right and (float_in_right or float_none):
            return [
                Particle(spill_right.x, spill_right.y, (spill_right.value + 1), 2)
            ]

    return []

def GetWaterLevel(value: float) -> float:
    return (value - Element.water.value)

def SetWaterLevel(current_value:float, spill_value: float) -> float:
    new_value: float = (current_value - spill_value)
    if new_value >= IsWater(new_value):
        return new_value
    
    return current_value

def CanWaterCombine(particle_directions: ParticleDirections) -> bool:
    is_water_below: bool = IsWater(particle_directions.vertical_down.value)
    water_below_value: float = particle_directions.vertical_down.value

    return is_water_below and Element.water.value <= water_below_value # < 22)

def CanWaterOverflow(particle_directions: ParticleDirections) -> bool:
    #is_water_below: bool = IsWater(particle_directions.current.value)
    water_cant_be_filled: bool = particle_directions.current.value > 22

    return water_cant_be_filled

def GetWaterFlowDirection(water: Particle) -> int:
    return water.flow_direction