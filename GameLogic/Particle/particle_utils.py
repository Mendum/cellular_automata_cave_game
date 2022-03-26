import numpy as np
import random
from GameLogic.Element.element import IsWater
from GameLogic.Particle.particle import Particle, ParticleDirections
from GameLogic.Element.element import IsRock, IsAir

def GetParticle(boards: np.ndarray, x: int, y: int) -> Particle:
    return Particle(x, y, GetParticleValue(boards, x, y), -1)

def GetParticleValue(boards: np.ndarray, x: int, y: int) -> float:
    return boards[x, y]

def GetParticleDirection(boards: np.ndarray, x: int, y: int) -> int:
    return boards[x, y].flow_direction

def SetParticlesDirections(boards: np.ndarray, x: int, y: int) -> ParticleDirections:
    return ParticleDirections(
        GetParticle(boards, x, y),
        GetParticle(boards, x, y-1),
        GetParticle(boards, x, y+1),
        GetParticle(boards, x+1, y),
        GetParticle(boards, x-1, y),
        GetParticle(boards, x+1, y-1),
        GetParticle(boards, x+1, y+1),
        GetParticle(boards, x-1, y-1),
        GetParticle(boards, x-1, y+1)
    )

def IsParticleFalling(board: np.ndarray, particle: Particle) -> bool:
    x = particle.x
    y = particle.y

    while not IsRock(GetParticleValue(board,x,y)):
        x = x + 1
        if IsAir(GetParticleValue(board,x,y)):
            return True
    
    return False

def RemoveEntity(movable_entites: list[Particle], particle: Particle) -> list[Particle]:
    return list(filter(lambda entity: not (entity.x == particle.x and entity.y == particle.y), movable_entites))

def ParticleCanMoveDown(particle_directions: ParticleDirections) -> bool:
    can_go_down: bool = IsAir(particle_directions.vertical_down.value)

    return can_go_down

def TryToMoveParticleDown(movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle) -> list[Particle]:
    if ParticleCanMoveDown(particle_directions):
        movable_entites = RemoveEntity(movable_entites, entity)
        movable_entites.append(Particle(entity.x+1, entity.y, entity.value, -1))

    return movable_entites

def ParticleCanMoveHorizontalIntoAir(particle_directions: ParticleDirections) -> bool:
    can_go_left: bool = IsAir(particle_directions.horizontal_left.value)
    can_go_right: bool = IsAir(particle_directions.horizontal_right.value)

    return (can_go_left or can_go_right)

def ParticleCanMoveHorizontalIntoWater(particle_directions: ParticleDirections) -> bool:
    can_go_left: bool = IsWater(particle_directions.horizontal_left.value)
    can_go_right: bool = IsWater(particle_directions.horizontal_right.value)

    return (can_go_left or can_go_right)

def ParticleMoveHorizontal(particle_directions: ParticleDirections) -> Particle:
    current: Particle = particle_directions.current
    left: Particle = particle_directions.horizontal_left
    right: Particle = particle_directions.horizontal_right

    return GenerateParticleDirectionHorizontal(left, right, current)

def ParticleCanMoveDiagonal(particle_directions: ParticleDirections) -> bool:
    can_go_left: bool = IsAir(particle_directions.diagonal_down_left.value)
    can_go_right: bool = IsAir(particle_directions.diagonal_down_right.value)

    return (can_go_left or can_go_right)

def ParticleMoveDiagonal(particle_directions) -> Particle:
    current: Particle = particle_directions.current
    left: Particle = particle_directions.diagonal_down_left
    right: Particle = particle_directions.diagonal_down_right
    GenerateParticleDirectionDiagonal(left, right, current)

    return GenerateParticleDirectionDiagonal(left, right, current)

def TryToMoveParticleDiagonal(movable_entites: list[Particle], particle_directions: ParticleDirections, entity: Particle, board: np.ndarray)  -> list[Particle]:
    if ParticleCanMoveDiagonal(particle_directions) and not IsParticleFalling(board, entity):
        movable_entites = RemoveEntity(movable_entites, entity)
        move_to = ParticleMoveDiagonal(particle_directions)
        movable_entites.append(Particle(move_to.x, move_to.y, entity.value, -1))
    
    return movable_entites

def GenerateRandomDirection(left: Particle, right: Particle) -> Particle:
    return right if random.random() > 0.5 else left

def GenerateParticleDirectionHorizontal(left: Particle, right: Particle, current: Particle) -> Particle:
    can_go_left: bool = IsWater(left.value)
    can_go_right: bool = IsWater(right.value)
    if can_go_left and can_go_right:
        return GenerateRandomDirection(left, right)

    elif can_go_left:
        return left

    elif can_go_right:
        return right
        
    return current

def GenerateParticleDirectionDiagonal(left: Particle, right: Particle, current: Particle) -> Particle:
    can_go_left: bool = IsAir(left.value)
    can_go_right: bool = IsAir(right.value)
    if can_go_left and can_go_right:
        return GenerateRandomDirection(left, right)

    elif can_go_left:
        return left

    elif can_go_right:
        return right
        
    return current