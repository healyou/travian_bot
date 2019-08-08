from enum import Enum


# в python не должно быть циклических зависимостей
def getBuildProductionTypes():
    return {
        Production.WOOD, 
        Production.CLAY, 
        Production.IRON,
        Production.CORN
    }


class Production(Enum):
    WOOD = 'wood'
    CLAY = 'clay'
    IRON = 'iron'
    CORN = 'corn'


class IndoorBuildingType(Enum):
    # амбар
    Stock = 'stock'