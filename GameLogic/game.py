from pprint import pprint
import numpy as np
from simulation.GameLogic.Element.element import LoadJsonFile
from simulation.board import Boards
from GameLogic.Particle.particle import Particle, ParticleDirections
from GameLogic.Particle.particle_utils import SetParticlesDirections
from GameLogic.Element.element_utils import GetAllMovableEntities
from GameLogic.gameFunctionality import functionality
from simulation.render import RenderNewBoard

# ne sme druga skrbet za drugo
# niti to ne: vsaka more bit odgovorna za sebe

def Play(boards: Boards) -> np.ndarray:
    movable_entitys = GetAllMovableEntities(boards)
    json_elements = LoadJsonFile()
    calculated_movable_entitys = SimulateParticleBehaviour(boards, movable_entitys, json_elements)

    return RenderNewBoard(boards, calculated_movable_entitys)

def SimulateParticleBehaviour(boards: Boards, movable_entites: list[Particle], json_elements) -> list[Particle]:

    temp_movable_entites: list = movable_entites

    #print('prej')
    #pprint(temp_movable_entites)
    for entity in movable_entites:
        particle_directions: ParticleDirections = SetParticlesDirections(boards.old_board, entity.x, entity.y)

        for element in json_elements:
            if element['value'] == entity.value:
                for behaviour in element['behaviours']:
                    for f in functionality:
                        if f.functionalityName == behaviour:
                            temp_movable_entites = f.functionalityFunction(temp_movable_entites, particle_directions, boards)
    #print('po')
    #pprint(temp_movable_entites)

    return temp_movable_entites