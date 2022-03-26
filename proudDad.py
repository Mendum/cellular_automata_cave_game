from dataclasses import dataclass
from genericpath import isfile
from multiprocessing.dummy import current_process
import random
from telnetlib import EL
from tkinter.tix import Tree
from more_itertools import random_combination_with_replacement
import numpy as np
from board import generateTempMap
from nptyping import NDArray, Float64
from enum import Enum

# ne sme druga skrbet za drugo
# vsaka more bit odgovorna za sebe

class Element(Enum):
    air = 0
    rock = 1
    water = 20
    wood = 30
    sand = 44
    fire = 50
    smoke = 60

@dataclass
class Cell:
    x: int
    y: int
    value: float

@dataclass
class Boards:
    old_board : np.ndarray
    temp_board : np.ndarray

@dataclass
class CellDirections:
    current: Cell
    horizontal_left: Cell
    horizontal_right: Cell
    vertical_down: Cell
    vertical_up: Cell
    diagonal_down_left: Cell
    diagonal_down_right: Cell
    diagonal_up_left: Cell
    diagonal_up_right: Cell

def Play(game_board: np.ndarray) -> np.ndarray:

    return Simulation(game_board)

def Simulation(old_board) -> np.ndarray:
    temp_board = generateTempMap() #  array z 0
    boards = Boards(old_board, temp_board)

    for x, y in np.ndindex(temp_board.shape):
        coordinates = SetCells(boards, x, y)
        SimulateCurrentCell(boards, coordinates)

    return boards.temp_board

def SetCells(boards: Boards, x, y) -> CellDirections:
    return CellDirections(
        GetCell(boards, x, y),
        GetCell(boards, x, y-1),
        GetCell(boards, x, y+1),
        GetCell(boards, x+1, y),
        GetCell(boards, x-1, y),
        GetCell(boards, x+1, y-1),
        GetCell(boards, x+1, y+1),
        GetCell(boards, x-1, y-1),
        GetCell(boards, x-1, y+1)
    )

def GetCell(boards: Boards, x: int, y: int) -> Cell:
    return Cell(x, y, CellValue(boards, x, y))

def RewriteCurrentCell(boards: Boards, cells: CellDirections, element_value: float) -> None:
    """
    ### Function:
    RewriteCoordinates will always rewrite current cell
    """
    boards.temp_board[cells.current.x, cells.current.y] = element_value

def CellValue(boards: Boards, x: int, y: int) -> float:
    return boards.old_board[x, y]

def SimulateCurrentCell(boards: Boards, cells: CellDirections) -> bool:

    if IsRock(cells.current.value):
        RewriteCurrentCell(boards, cells, Element.rock.value)
        return True
    
    if IsAir(cells.current.value):
        SimulateAir(boards, cells)
        return True
    
    print('300 kosmatih medvedov')
    return False

def SimulateAir(boards: Boards, cells: CellDirections) -> bool:

    if IsWood(cells.vertical_up.value):
        RewriteCurrentCell(boards, cells, Element.wood.value)
        return True

    #if IsWater(coordinate_current_value):
    #    if is_water_above_me:
    #        RewriteCurrentCell(boards, cells, coordinate_above_value)

    #if IsAir(coordinate_below_value):
    #    RewriteCurrentCell(boards, cells, Element.air.value)
    #    return True

    #elif IsWater(coordinate_below_value) and IsWater(coordinate_value):
    #    WaterFill(boards, cells, coordinate_value)

    #elif IsWater(coordinate_below_value) and IsFire(coordinate_value):
    #    dark_smoke = 61
    #    SmokeFill(boards, cells, dark_smoke)

    #elif IsWood(coordinate_below_value) and IsFire(coordinate_value):
    #    light_smoke = 60
    #    SmokeFill(boards, cells, light_smoke)
        #ElementMoveDiagonal()

    return False

def ElementMoveUp(boards: Boards, coordinates_directions: CellDirections) -> bool:

    if IsAir(coordinate_above_value):
        RewriteCurrentCell(boards, element_above, coordinate_value)
        return True
    
    return False

def ElementMoveDiagonal(boards: Boards, coordinates_directions: CellDirections) -> bool:

    canGoLeft: bool = CellValue(boards, coordinates_directions.diagonal_down_left) == 0
    canGoRight: bool = CellValue(boards, coordinates_directions.diagonal_down_right) == 0
    coordinate_value = CellValue(boards, coordinates_directions.current)

    if canGoLeft and canGoRight:
        rnd = random.random()
        if rnd > 0.5:
            RewriteCurrentCell(boards, coordinates_directions.diagonal_down_right, coordinate_value)
            return True
        else:
            RewriteCurrentCell(boards, coordinates_directions.diagonal_down_left, coordinate_value)
            return True

    elif canGoLeft:
        RewriteCurrentCell(boards, coordinates_directions.diagonal_down_left, coordinate_value)
        return True

    elif canGoRight:
        RewriteCurrentCell(boards, coordinates_directions.diagonal_down_right, coordinate_value)
        return True

    return False

def ElementMoveHorizontal(boards: Boards, coordinates_directions: CellDirections, element_value: float) -> bool:

    canGoLeft: bool = CellValue(boards, coordinates_directions.horizontal_left) == 0
    canGoRight: bool = CellValue(boards, coordinates_directions.horizontal_right) == 0
    coordinate_value = CellValue(boards, coordinates_directions.current)

    if canGoLeft or canGoRight:
        if IsWater(element_value):
            return WaterSpill(boards, coordinates_directions)
        
        if IsFire(element_value):
            return FireSpread(boards, coordinates_directions)
    
    return False

def WaterSpill(boards: Boards, coordinates_directions: CellDirections) -> bool:

    coordinate_value = CellValue(boards, coordinates_directions.current)
    
    #print('Moj level je:', GetWaterLevel(coordinate_value))

    match GetWaterLevel(coordinate_value):
        case 0:
            #print("spill 0000")
            new_water_level = setWaterLevel(coordinate_value, 0)
            GenerateWaterParticle(boards, coordinates_directions.current, new_water_level)
            return True

        case 1:
            rnd = random.random()
            if rnd > 0.5:
                #print("spill right")
                new_water_level = setWaterLevel(coordinate_value, 1)
                GenerateWaterParticle(boards, coordinates_directions.current, new_water_level)
                GenerateWaterParticle(boards, coordinates_directions.horizontal_right, new_water_level)
                return True
            else:
                #print("spill left")
                new_water_level = setWaterLevel(coordinate_value, 1)
                GenerateWaterParticle(boards, coordinates_directions.current, new_water_level)
                GenerateWaterParticle(boards, coordinates_directions.horizontal_left, new_water_level)
                return True

        case 2:
            #print("spill both")
            new_water_level = setWaterLevel(coordinate_value, 2)
            #print('prepisujem trenutne: ')
            #print(f'x: {coordinates_directions.current.x} y: {coordinates_directions.current.y}')
            GenerateWaterParticle(boards, coordinates_directions.current, new_water_level)

            #print('prepisujem levo: ')
            #print(f'x: {coordinates_directions.horizontal_left.x} y: {coordinates_directions.horizontal_left.y}')
            GenerateWaterParticle(boards, coordinates_directions.horizontal_left, new_water_level)

            #print('prepisujem desno: ')
            #print(f'x: {coordinates_directions.horizontal_right.x} y: {coordinates_directions.horizontal_right.y}')
            GenerateWaterParticle(boards, coordinates_directions.horizontal_right, new_water_level)

            return True

    return False

def GetWaterLevel(value: float) -> float:
    return (value - 20)

def setWaterLevel(current_value:float, spill_value: float) -> float:
    new_value = (current_value - spill_value)
    if new_value >= IsWater(new_value):
        return new_value
    
    return current_value

def WaterOverflow(boards: Boards, coordinates: Cell, water_level: float):
    GenerateWaterParticle(boards, coordinates, water_level)

def WaterFill(boards: Boards, coordinates_directions: CellDirections, element_value: float) -> bool:
    if IsWater(element_value):
        GenerateWaterParticle(boards, coordinates_directions.current, element_value)
    if element_value > 22:
        GenerateWaterParticle(boards, coordinates_directions.vertical_up, element_value)
        return True
    
    return False

def GenerateWaterParticle(boards: Boards, coordinates: Cell, element_value: float):
    RewriteCurrentCell(boards, coordinates, element_value)

def GenerateWoodParticle(boards: Boards, coordinates: Cell, element_value: float):
    RewriteCurrentCell(boards, coordinates, element_value)

def GenerateSandParticle(boards: Boards, coordinates: Cell, element_value: float):
    RewriteCurrentCell(boards, coordinates, element_value)

def GenerateFireParticle(boards: Boards, coordinates: Cell, element_value: float):
    RewriteCurrentCell(boards, coordinates, element_value)

def GenerateSmokeParticle(boards: Boards, coordinates: Cell, element_value: float):
    print('in rad bi naredo smoke particle')
    print(element_value)
    RewriteCurrentCell(boards, coordinates, element_value)

def SmokeFill(boards: Boards, coordinates_directions: CellDirections, element_value: float) -> bool:

    if ElementMoveUp(boards, coordinates_directions):
        GenerateSmokeParticle(boards, coordinates_directions.vertical_up, element_value)
        return True
    
    return False

def FireSpread(boards: Boards, coordinates_directions: CellDirections) -> bool:

    return False

    #if IsWater(element_value):
    #    GenerateWaterParticle(boards, coordinates_directions.current, element_value)
    #if element_value > 22:
    #    GenerateWaterParticle(boards, coordinates_directions.vertical_up, element_value)
    #    return True
    
    return False

def IsAir(value: float) -> bool:
    return (value == 0)

def IsRock(value: float) -> bool:
    return (value == 1)

def IsWater(value: float) -> bool:
    return (value >= 20 and value <= 22)

def IsWood(value: float) -> bool:
    return (value == 30)

def IsSand(value: float) -> bool:
    return (value == 40)

def IsFire(value: float) -> bool:
    return (value == 50)

def IsSmoke(value: float) -> bool:
    return (value >= 60 and value <= 61)

def SimulateElement(boards: Boards, coordinates_directions: CellDirections, element_value: float) -> None:

    coordinate_value = CellValue(boards, coordinates_directions.current)

    if IsWater(element_value):
        Water(boards, coordinates_directions)

    if IsWood(element_value):
        Wood(boards, coordinates_directions)

    if IsSand(element_value):
        Sand(boards, coordinates_directions)

    if IsFire(element_value):
        Fire(boards, coordinates_directions)
    
    if IsSmoke(element_value):
        Smoke(boards, coordinates_directions)

def Water(boards: Boards, coordinates_directions: CellDirections) -> bool:
    if ElementMoveDown(boards, coordinates_directions):
        return True
    
    elif ElementMoveDiagonal(boards, coordinates_directions):
        return True

    elif ElementMoveHorizontal(boards, coordinates_directions, Element.water.value):
        return True

    return False

def Wood(boards: Boards, coordinates_directions: CellDirections) -> bool:
    if ElementMoveDown(boards, coordinates_directions):
        return True
    
    return False

def Sand(boards: Boards, coordinates_directions: CellDirections) -> bool:
    if ElementMoveDown(boards, coordinates_directions):
        return True
    
    elif ElementMoveDiagonal(boards, coordinates_directions):
        return True
    
    return False

def Fire(boards: Boards, coordinates_directions: CellDirections) -> bool:
    if ElementMoveDown(boards, coordinates_directions):
        return True
    
    return False

def Smoke(boards: Boards, coordinates_directions: CellDirections) -> bool:
    if ElementMoveUp(boards, coordinates_directions):
        return True
    
    return False