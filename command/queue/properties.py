from utils.util import getVillagesCoords
from collections import namedtuple
import datetime


BuildProperties = namedtuple('BuildProperties', [
    # Автоматическое строительство ресурсов
    'auto_build_resources',
    # Время строительства следующего здания
    'next_build_time'
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
            properties.append((VillageCoord(x, y), BuildProperties(True, datetime.today())))

        self.__properties = properties

    def getVillageProperties(self, x, y) -> BuildProperties:
        for (vil_coord, prop) in self.__properties:
            if (vil_coord.x == x and vil_coord.y == y):
                return prop
        raise Exception('Деревня не найдена')
    
    def getNextBuildTime(self, x, y):
        for (vil_coord, prop) in self.__properties:
            if (vil_coord.x == x and vil_coord.y == y):
                return prop.next_build_time
        raise Exception('Деревня не найдена')

# TODO - добавить очередь на строительство в деревни
# TODO 1) Автоматически строим поля в деревни
# TODO 2) Когда стоимость строительства поля на 60% превысила лимит склада - развиваем склад (но не более 80000 вместимости склада)
# TODO 3) Строить по времени строительства след. здания - если ничего не строится - строим здание и запоминаем время окончания для деревни