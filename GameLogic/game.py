from pprint import pprint
import numpy as np
from simulation.GameLogic.Element.element import LoadJsonFile
from simulation.GameLogic.Element.smoke import TryToSmokeDark
from simulation.GameLogic.Particle.particle_utils import RemoveEntity, TryToMoveParticleDiagonal, TryToMoveParticleDown
from simulation.board import RenderNewBoard
from GameLogic.Particle.particle import Particle, ParticleDirections
from GameLogic.Particle.particle_utils import SetParticlesDirections
#from GameLogic.Element.element import IsWater, IsSand, IsWood, IsWoodBurned, IsFire, IsSmokeLight, IsSmokeDark
from GameLogic.Element.element_utils import GetAllMovableEntities
from simulation.GameLogic.Element.water import TryToCombineWater, TryToDisplacesWater, TryToDisplacesWood, TryToOverflowWater, TryToSpillWaterIntoAir, TryToSpillWaterIntoWater#, Water
#from simulation.GameLogic.Element.sand import Sand
#from simulation.GameLogic.Element.wood import Wood, WoodBurned
#from simulation.GameLogic.Element.fire import Fire, TryToExtinguishFire, TryToSpreadFire
from simulation.GameLogic.Element.fire import TryToExtinguishFire, TryToSpreadFire
#from simulation.GameLogic.Element.smoke import SmokeDark, SmokeLight
#from simulation.GameLogic.Element.grass import Grass

# ne sme druga skrbet za drugo
# niti to ne: vsaka more bit odgovorna za sebe

def Play(board: np.ndarray) -> np.ndarray:
    movable_entitys = GetAllMovableEntities(board)
    json_elements = LoadJsonFile()
    calculated_movable_entitys = SimulateParticleBehaviour(board, movable_entitys, json_elements)

    return RenderNewBoard(board, calculated_movable_entitys)

def SimulateParticleBehaviour(board: np.ndarray, movable_entites: list[Particle], json_elements) -> list[Particle]:

    temp_movable_entites: list = movable_entites

    pprint(temp_movable_entites)
    for entity in movable_entites:
        particle_directions: ParticleDirections = SetParticlesDirections(board, entity.x, entity.y)

        for element in json_elements:
            if element['value'] == entity.value:
                for behaviour in element['behaviours']:
                    match behaviour:
                        case 'TryToMoveParticleDown':
                            temp_movable_entites = TryToMoveParticleDown(temp_movable_entites, particle_directions, entity)
                        
                        # wood burned
                        case 'RemoveEntity':
                            temp_movable_entites = RemoveEntity(temp_movable_entites, entity)

                        # sand
                        case 'TryToDisplacesWater':
                            temp_movable_entites = TryToDisplacesWater(temp_movable_entites, particle_directions, entity, board)
                        
                        # sand
                        case 'TryToMoveParticleDiagonal':
                            temp_movable_entites = TryToMoveParticleDiagonal(temp_movable_entites, particle_directions, entity, board)
                        
                        # fire
                        case 'TryToExtinguishFire':
                            temp_movable_entites = TryToExtinguishFire(board, temp_movable_entites, entity, particle_directions)
                        
                        # fire
                        case 'TryToSpreadFire':
                            temp_movable_entites = TryToSpreadFire(temp_movable_entites, particle_directions, entity)
                        
                        # smoke
                        case 'TryToSmokeDark':
                            temp_movable_entites = TryToSmokeDark(movable_entites, entity)
                            
                        # water
                        case 'TryToCombineWater':
                            temp_movable_entites = TryToCombineWater(temp_movable_entites, particle_directions, entity, board)
                            
                        # water
                        case 'TryToOverflowWater':
                            temp_movable_entites = TryToOverflowWater(temp_movable_entites, particle_directions, entity)
                            
                        # water
                        case 'TryToDisplacesWood':
                            temp_movable_entites = TryToDisplacesWood(temp_movable_entites, particle_directions, entity, board)
                            
                        # water
                        case 'TryToSpillWaterIntoAir':
                            temp_movable_entites = TryToSpillWaterIntoAir(temp_movable_entites, particle_directions, entity, board)
                            
                        # water
                        case 'TryToSpillWaterIntoWater':
                            temp_movable_entites = TryToSpillWaterIntoWater(temp_movable_entites, particle_directions, entity, board)

    return temp_movable_entites