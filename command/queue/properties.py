from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from utils.context import Context
from utils.util import getVillagesCoords


# Свойства строительства в деревне
@dataclass
class VillageBuildProperties:
    # Автоматическое строительство ресурсов
    auto_build_resources: bool = False
    # Время строительства следующего здания
    next_build_datetime: Any = None
    # Необходимость строительства склада или амбара
    # None - ничего, True - Stock, False - Granary
    is_stock_or_granary_build: bool = None


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
            build_properties = VillageBuildProperties(False, datetime.today(), None)
            point = Point(x, y)
            data = VillageData(build_properties, point)

            properties.append(data)
        self.__properties = properties

    def getVillageProperties(self, coord: Point) -> VillageBuildProperties:
        for data in self.__properties:
            if (data.point.x == coord.x and data.point.y == coord.y):
                return data.prop
        raise Exception('Деревня не найдена')

    def setVillageProperties(self, coord: Point, prop: VillageBuildProperties):
        for data in self.__properties:
            if (data.point.x == coord.x and data.point.y == coord.y):
                data.prop = prop
                print ('Свойства изменены')
        raise Exception('Деревня не найдена')
    
    def getNextBuildTime(self, x: int, y: int):
        for data in self.__properties:
            if (data.point.x == x and data.point.y == y):
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

    # None - ничего, True - Stock, False - Granary
    def __setStockOrGranaryBuild(self, value: bool):
        prop = self.__queue_prop
        vil_prop: VillageBuildProperties = prop.getVillageProperties(self.__coord)
        # Изменить свойство и в начальном объекте (одна область памяти)
        vil_prop.is_stock_or_granary_build = value

# TODO - добавить очередь на строительство в деревни
# TODO 2) Когда стоимость строительства поля на 60% превысила лимит склада - развиваем склад (но не более 80000 вместимости склада)
# TODO 3) Строить по времени строительства след. здания - если ничего не строится - строим здание и запоминаем время окончания для деревни
