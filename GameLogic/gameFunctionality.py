from dataclasses import dataclass
from typing import Callable
from GameLogic.Particle.particle import Particle, ParticleDirections
from simulation.GameLogic.Element.fire import TryToExtinguishFire, TryToSpreadFire
from simulation.GameLogic.Element.smoke import TryToSmokeDark, TryToSmokeLight
from simulation.GameLogic.Element.water import TryToCombineWater, TryToDisplacesWater, TryToDisplacesWood, TryToOverflowWater, TryToSpillWaterIntoAir, TryToSpillWaterIntoWater
from simulation.GameLogic.Particle.particle_utils import TryToMoveParticleDiagonal, TryToMoveParticleDown
from simulation.board import Boards


@dataclass
class Functionality:
    functionalityName: str
    functionalityFunction: Callable[[list[Particle], ParticleDirections, Boards],list[Particle]]

functionality: list[Functionality] = [
    Functionality("TryToMoveParticleDown", TryToMoveParticleDown),
    Functionality("TryToMoveParticleDiagonal", TryToMoveParticleDiagonal),
    Functionality("TryToExtinguishFire", TryToExtinguishFire),
    Functionality("TryToSpreadFire", TryToSpreadFire),
    Functionality("TryToSmokeLight", TryToSmokeLight),
    Functionality("TryToSmokeDark", TryToSmokeDark),
    Functionality("TryToCombineWater", TryToCombineWater),
    Functionality("TryToOverflowWater", TryToOverflowWater),
    Functionality("TryToDisplacesWater", TryToDisplacesWater),
    Functionality("TryToDisplacesWood", TryToDisplacesWood),
    Functionality("TryToSpillWaterIntoAir", TryToSpillWaterIntoAir),
    Functionality("TryToSpillWaterIntoWater", TryToSpillWaterIntoWater),
]