import numpy as np
from simulation.GameLogic.Element.element import IsGrass
from simulation.board import RenderNewBoard
from GameLogic.Particle.particle import Particle, ParticleDirections
from GameLogic.Particle.particle_utils import SetParticlesDirections
from GameLogic.Element.element import IsWater, IsSand, IsWood, IsWoodBurned, IsFire, IsSmokeLight, IsSmokeDark
from GameLogic.Element.element_utils import GetAllMovableEntities
from simulation.GameLogic.Element.water import Water
from simulation.GameLogic.Element.sand import Sand
from simulation.GameLogic.Element.wood import Wood, WoodBurned
from simulation.GameLogic.Element.fire import Fire
from simulation.GameLogic.Element.smoke import SmokeDark, SmokeLight
from simulation.GameLogic.Element.grass import Grass

# ne sme druga skrbet za drugo
# niti to ne: vsaka more bit odgovorna za sebe

def Play(board: np.ndarray) -> np.ndarray:
    movable_entitys = GetAllMovableEntities(board)
    calculated_movable_entitys = SimulateParticleBehaviour(board, movable_entitys)

    return RenderNewBoard(board, calculated_movable_entitys)

def SimulateParticleBehaviour(board: np.ndarray, movable_entites: list[Particle]) -> list[Particle]:

    temp_movable_entites: list = movable_entites

    for entity in movable_entites:
        particle_directions: ParticleDirections = SetParticlesDirections(board, entity.x, entity.y)

        if IsWater(entity.value):
            temp_movable_entites = Water(temp_movable_entites, particle_directions, board, entity)

        elif IsSand(entity.value):
            temp_movable_entites = Sand(temp_movable_entites, particle_directions, board, entity)

        elif IsWood(entity.value):
            temp_movable_entites = Wood(temp_movable_entites, particle_directions, entity)

        elif IsWoodBurned(entity.value):
            temp_movable_entites = WoodBurned(temp_movable_entites, entity)
        
        elif IsFire(entity.value):
            temp_movable_entites = Fire(temp_movable_entites, particle_directions, board, entity)

        elif IsSmokeLight(entity.value):
            temp_movable_entites = SmokeLight(temp_movable_entites, entity)

        elif IsSmokeDark(entity.value):
            temp_movable_entites = SmokeDark(temp_movable_entites, entity)

        elif IsGrass(entity.value):
            temp_movable_entites = Grass(temp_movable_entites, particle_directions, board, entity)

    return temp_movable_entites