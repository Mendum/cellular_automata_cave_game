from enum import Enum
import json

class Element(Enum):
    air = 0
    rock = 1
    water = 20
    sand = 30
    wood = 40
    wood_burned = 41
    fire = 50
    smoke_light = 60
    smoke_dark = 61

def LoadJsonFile():
    with open('elementsConfig.json') as f:
        data = json.load(f)
        return data

json_elements = LoadJsonFile()

def FindRockInJson(json_elements):
    for element in json_elements:
        if element['name'] == "rock":
            return element

def FindAirInJson(json_elements):
    for element in json_elements:
        if element['name'] == "air":
            return element

def IsAir(value: float) -> bool:
    return (value == Element.air.value)
    #rock_element = FindRockInJson(json_elements)
    #return rock_element['value'] == value

def IsRock(value: float) -> bool:
    return (value == Element.rock.value)
    #rock_element = FindAirInJson(json_elements)
    #return rock_element['value'] == value

def IsWater(value: float) -> bool:
    return (value >= 20 and value <= 22)

def IsWood(value: float) -> bool:
    return (value == Element.wood.value)

def IsWoodBurned(value: float) -> bool:
    return (value == Element.wood_burned.value)

def IsSand(value: float) -> bool:
    return (value == Element.sand.value)

def IsFire(value: float) -> bool:
    return (value == Element.fire.value)

def IsSmokeLight(value: float) -> bool:
    return (value == Element.smoke_light.value)

def IsSmokeDark(value: float) -> bool:
    return (value == Element.smoke_dark.value)