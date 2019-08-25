from utils.util import getVillagesCoords
from collections import namedtuple
from datetime import datetime
from utils.context import Context


BuildProperties = namedtuple('BuildProperties', [
    # Автоматическое строительство ресурсов
    'auto_build_resources',
    # Время строительства следующего здания
    'next_build_datetime',
    # Необходимость строительства склада или амбара
    # None - ничего, True - Stock, False - Granary
    'is_stock_or_granary_build'
])
VillageCoord = namedtuple('VillageCoord', [
    'x', 'y'
])
# Параметры задач бота
class QueueProperties(object):
    def __init__(self, browser):
        super(QueueProperties, self).__init__()

        villages_coords = getVillagesCoords(browser)
        properties = []
        for (x, y) in villages_coords:
            properties.append((VillageCoord(x, y), BuildProperties(
                True, datetime.today(), None
            )))

        self.__properties = properties

    def getVillageProperties(self, x, y) -> BuildProperties:
        for (vil_coord, prop) in self.__properties:
            if (vil_coord[0] == x and vil_coord[1] == y):
                return prop
        raise Exception('Деревня не найдена')

    def setVillageProperties(self, x, y, prop):
        for value in self.__properties:
            if (value[0][0] == x and value[0][1] == y):
                # TODO - нельзя изменять кортежи - поменять на классы
                value[1] = prop
                print ('Свойства изменены')
        raise Exception('Деревня не найдена')
    
    def getNextBuildTime(self, x, y):
        for (vil_coord, prop) in self.__properties:
            if (vil_coord[0] == x and vil_coord[1] == y):
                return prop.next_build_time
        raise Exception('Деревня не найдена')


# Класс, позволяющий деревне управлять её свойствами
class VillageProperties(object):
    def __init__(self, coordX, coordY):
        super(VillageProperties, self).__init__()
        self.__coord = VillageCoord(coordX, coordY)
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
        # TODO - изменить на св-ва 
        vil_prop = prop.getVillageProperties(self.__coord[0], self.__coord[1])
        new_prop = BuildProperties(vil_prop[0], vil_prop[1], value)
        prop.setVillageProperties(self.__coord[0], self.__coord[1], new_prop)

        vil_prop = prop.getVillageProperties(self.__coord[0], self.__coord[1])
        k = 1

# TODO - добавить очередь на строительство в деревни
# TODO 2) Когда стоимость строительства поля на 60% превысила лимит склада - развиваем склад (но не более 80000 вместимости склада)
# TODO 3) Строить по времени строительства след. здания - если ничего не строится - строим здание и запоминаем время окончания для деревни