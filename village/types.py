from enum import Enum
from collections import namedtuple


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


ProductionTuple = namedtuple('Test', ['code', 'displayName'])
class Production(Enum):
    WOOD = ProductionTuple('wood', 'Лесопилка')
    CLAY = ProductionTuple('clay', 'Глиняный карьер')
    IRON = ProductionTuple('iron', 'Железный рудник')
    CORN = ProductionTuple('corn', 'Ферма')

    @property
    def code(self) -> str:
        return self.value.code

    @property
    def displayName(self) -> str:
        return self.value.displayName


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