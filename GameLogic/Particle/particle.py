from dataclasses import dataclass

@dataclass
class Particle:
    x: int
    y: int
    value: float
    flow_direction: int # -1 ne tece ... 1 levo, 2 desno, 3 diagonalno dol levo, 4 diagonalno dol desno, 5 gor

@dataclass
class ParticleDirections:
    current: Particle
    horizontal_left: Particle
    horizontal_right: Particle
    vertical_down: Particle
    vertical_up: Particle
    diagonal_down_left: Particle
    diagonal_down_right: Particle
    diagonal_up_left: Particle
    diagonal_up_right: Particle
