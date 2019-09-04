from collections import deque, namedtuple
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from command.commands import AbstractCommand
from utils.context import Context
from utils.util import getVillagesCoords


# Свойства строительства в деревне
@dataclass
class VillageBuildProperties:
    # Автоматическое строительство ресурсов
    auto_build_resources: bool
    # Время строительства следующего здания
    next_build_datetime: datetime
    # Необходимость строительства склада или амбара
    # None - ничего, True - Stock, False - Granary
    is_stock_or_granary_build: bool


@dataclass
class Point:
    x: int
    y: int


# Данные деревни
@dataclass
class VillageData:
    prop: VillageBuildProperties
    point: Point


# Параметры задач бота
class QueueProperties(object):
    def __init__(self, browser):
        super(QueueProperties, self).__init__()

        villages_coords = getVillagesCoords(browser)
        properties = []
        for (x, y) in villages_coords:
            build_properties = VillageBuildProperties(True, datetime.today(), None)
            point = Point(x, y)
            data = VillageData(build_properties, point)

            properties.append(data)
        self.__properties = properties
        # Очередь выполнения команд строительства
        self.__build_commands_deque = deque()

    def analizeAutoBuildForAllVillages(self):
        deque = self.__build_commands_deque
        from village.command.commands import AutoBuildProductionFieldCommand, BuildVillageBuildingCommand
        from village.types import IndoorBuildingType

        for vil_data in self.__properties:
            build_prop: VillageBuildProperties = vil_data.prop
            coord: Point = vil_data.point

            # Необходимость автоматического строительства ресурсов
            if (not build_prop.auto_build_resources):
                continue

            # Необходимость строить склад или амбар
            if(build_prop.is_stock_or_granary_build is not None):
                # True - Stock, False - Granary
                if (build_prop.is_stock_or_granary_build):
                    command = BuildVillageBuildingCommand(IndoorBuildingType.STOCK, coord.x, coord.y)
                    build_prop.is_stock_or_granary_build = None
                else:
                    command = BuildVillageBuildingCommand(IndoorBuildingType.GRANARY, coord.x, coord.y)
                    build_prop.is_stock_or_granary_build = None
                    
                deque.append(command)
                continue

            # Автоматическое строительство ресурсов
            next_build_dt: datetime = build_prop.next_build_datetime
            if (next_build_dt <= datetime.now()):
                command = AutoBuildProductionFieldCommand(coord.x, coord.y)
                deque.append(command)

    def getNextBuildingCommand(self) -> AbstractCommand:
        deque = self.__build_commands_deque
        if (len(deque) > 0):
            command = self.__build_commands_deque.popleft()
            return command
        else:
            return None

    def getVillageProperties(self, coord: Point) -> VillageBuildProperties:
        for data in self.__properties:
            vil_coord = data.point
            if (vil_coord.x == coord.x and vil_coord.y == coord.y):
                return data.prop
        raise Exception('Деревня не найдена')

    def setVillageProperties(self, coord: Point, prop: VillageBuildProperties):
        for data in self.__properties:
            vil_coord = data.point
            if (vil_coord.x == coord.x and vil_coord.y == coord.y):
                data.prop = prop
                print ('Свойства изменены')
        raise Exception('Деревня не найдена')
    
    def getNextBuildTime(self, x: int, y: int):
        for data in self.__properties:
            vil_coord = data.point
            if (vil_coord.x == x and vil_coord.y == y):
                return data.prop.next_build_time
        raise Exception('Деревня не найдена')


# Класс, позволяющий деревне управлять её свойствами
class VillageProperties(object):
    def __init__(self, coordX, coordY):
        super(VillageProperties, self).__init__()
        self.__coord: Point = Point(coordX, coordY)
        self.__queue_prop: QueueProperties = Context.queueProperties

    def setNeedBuildStock(self):
        print ('Необходимо строить склад')
        self.__setStockOrGranaryBuild(True)

    def setNeedBuildGranary(self):
        print ('Необходимо строить амбар')
        self.__setStockOrGranaryBuild(False)

    def setNextBuildDatetime(self, dt: datetime):
        vil_prop: VillageBuildProperties = self.__getVillageProperties()
        # Изменить свойство и в начальном объекте (одна область памяти)
        vil_prop.next_build_datetime = dt

    # None - ничего, True - Stock, False - Granary
    def __setStockOrGranaryBuild(self, value: bool):
        vil_prop: VillageBuildProperties = self.__getVillageProperties()
        # Изменить свойство и в начальном объекте (одна область памяти)
        vil_prop.is_stock_or_granary_build = value

    def __getVillageProperties(self) -> VillageBuildProperties:
        prop = self.__queue_prop
        return prop.getVillageProperties(self.__coord)
