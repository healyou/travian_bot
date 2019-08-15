from command.commands import AbstractCommand
from command.creator.factory import JsonCommandCreator
from utils.context import Context
from utils.util import convert_str_with_one_number_to_int as toInt
import re
from element.elements import BaseElement
from selector.selectors import ProductionFieldSelector, IndoorBuildingSelector
from village.types import Production, IndoorBuildingType
from village.building.buildings import buildExitingFieldWithRaiseException, buildNewVillageBuildingsWithRaiseException
from village.visitors import BuildFieldExceptionVisitor
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType


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


class BuildVillageBuildingCommand(AbstractCommand): 
    def __init__(self, type: IndoorBuildingType, lvl: int, vilX: int, vilY: int): 
        super(BuildVillageBuildingCommand, self).__init__() 
        self.__type: IndoorBuildingType = type 
        self.__lvl: int = lvl 
        self.__browser = Context.browser 
        self.__open_vil_command: AbstractCommand = OpenVillageCommand(vilX, vilY) 
        self.__open_vil_buildings_command: AbstractCommand = OpenVillageBuildingsCommand() 
    
    def execute(self): 
        # TODO - надо ли ждать загрузки страницы? 
        self.__open_vil_command.execute() 
        self.__open_vil_buildings_command.execute() 
        self.__buildField() 
    
    def __buildField(self): 
        try: 
            # Находим нужное поле 
            browser = Context.browser 
            selector = IndoorBuildingSelector(browser, self.__type, self.__lvl) 
            selector.findElement()

            # Открываем окно строительства
            selector.clickToElement()

            name = selector.getFieldName()

            if (selector.isExitingBuilding()):
                # Увеличиваем уровень здания
                buildExitingFieldWithRaiseException(self.__browser, name) 
            else:
                # Строим новое здания из окно выбора строений
                buildNewVillageBuildingsWithRaiseException(self.__browser, self.__type, name)

        except BuildFieldException as err: 
            err.accept(BuildFieldExceptionVisitor())


# Строит ресурсное поле
class BuildProductionFieldCommand(AbstractCommand): 
    def __init__(self, type: Production, lvl: int, vilX: int, vilY: int): 
        super(BuildProductionFieldCommand, self).__init__() 
        self.__type: Production = type 
        self.__lvl: int = lvl
        self.__browser = Context.browser
        self.__open_vil_command: AbstractCommand = OpenVillageCommand(vilX, vilY)
        self.__open_resources_command: AbstractCommand = OpenVillageResourcesCommand()

    def execute(self):
        # TODO - надо ли ждать загрузки страницы?
        self.__open_vil_command.execute()
        self.__open_resources_command.execute()
        self.__buildField()

    def __buildField(self):
        try:
            # Находим нужное поле
            field = self.__getField()
            name = field.get_attribute('alt')
            # Открываем окно строительства поля
            field.click()
            # Строим в окне строительства
            buildExitingFieldWithRaiseException(self.__browser, name)
        except BuildFieldException as err:
            err.accept(BuildFieldExceptionVisitor())

    def __getField(self):
        browser = Context.browser
        selector = ProductionFieldSelector(browser, self.__type, self.__lvl)
        elem = BaseElement(browser, selector)
        return elem.getElement()


# TODO - что надо реализовать по постройке полей
# общий план таков: 
# Команда на строительство полей: тип строительства(внутри или снаружи деревни)
#   Тип поля - ресурсное какое или внутри поле
#   Уровень поля - так можно будет строить поля, если одинаковых 2 и более
#   Привязана также к какой-то деревне - по атрибутам, чтобы строить в конкретной здание
# FieldFinder - найдёт компонент поля по заданным параметра, по котормоу можно кликнуть и начать строить