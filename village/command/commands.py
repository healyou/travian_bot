from command.commands import AbstractCommand
from command.creator.factory import JsonCommandCreator
from utils.context import Context
from utils.util import convert_str_with_one_number_to_int as toInt
import re


# Открывает ресурсные поля в выбранной деревне
class OpenVillageResourcesCommand(AbstractCommand):
    def __init__(self):
        super(OpenVillageResourcesCommand, self).__init__()

    def execute(self):
        creator = JsonCommandCreator(Context.browser, 'files/travian/open_resources.json')
        command = creator.createCommand()
        command.execute()


# Открывает внутреннюю часть деревни
class OpenVillageBuildingsCommand(AbstractCommand):
    def __init__(self):
        super(OpenVillageBuildingsCommand, self).__init__()
        
    def execute(self):
        creator = JsonCommandCreator(Context.browser, 'files/travian/open_village.json')
        command = creator.createCommand()
        command.execute()


# Открывает страницу выбранной деревни
class OpenVillageCommand(AbstractCommand):
    def __init__(self, coordX, coordY):
        super(OpenVillageCommand, self).__init__()
        self.__coordX = coordX
        self.__coordY = coordY

    def execute(self):
        browser = Context.browser
        css = '#sidebarBoxVillagelist > .sidebarBoxInnerBox > .content > ul > li'
        elems = browser.find_elements_by_css_selector(css)
        for elem in elems:
            # TODO - поиск деревни по заданным параметрам
            xComp = elem.find_element_by_css_selector('.coordinates > .coordinateX')
            yComp = elem.find_element_by_css_selector('.coordinates > .coordinateY')
            
            vilX = toInt(xComp.text)
            vilY = toInt(yComp.text)
            
            if (self.__coordX == vilX and self.__coordY == vilY):
                vil_link = elem.find_element_by_css_selector('a')
                vil_link.click()
                return
        raise Exception('Не найдена деревня')

# TODO - что надо реализовать по постройке полей
# общий план таков: 
# Команда на строительство полей: тип строительства(внутри или снаружи деревни)
#   Тип поля - ресурсное какое или внутри поле
#   Уровень поля - так можно будет строить поля, если одинаковых 2 и более
#   Привязана также к какой-то деревне - по атрибутам, чтобы строить в конкретной здание
# FieldFinder - найдёт компонент поля по заданным параметра, по котормоу можно кликнуть и начать строить