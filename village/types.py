from enum import Enum


# в python не должно быть циклических зависимостей
def getBuildProductionTypes():
    return {
        Production.WOOD, 
        Production.CLAY, 
        Production.IRON,
        Production.CORN
    }


class BuildType(Enum): 
    # Ресурсное поле 
    RESOURCES = 'resources' 
    # Строения внутри деревни 
    BUILDINGS = 'buildings'


class Production(Enum):
    WOOD = 'wood'
    CLAY = 'clay'
    IRON = 'iron'
    CORN = 'corn'


class IndoorBuildingType(Enum):
    # Склад
    Stock = 'stock'
    # Амбар
    GRANARY = 'granary'
    # Резиденция
    RESIDENCE = 'residence'
    # Изгородь
    HEDGE = 'hedge'
    # Мастерская
    WORKSHOP = 'workshop'