import re
from abc import abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType

from command.commands import AbstractCommand
from command.creator.factory import JsonCommandCreator
from element.elements import BaseElement
from selector.selectors import (AbstractSelector, IndoorBuildingSelector,
                                ProductionFieldSelector, 
                                ProductionFieldWithSmallLevelSelector)
from utils.context import Context
from utils.util import convert_str_with_one_number_to_int as toInt
from village.building.buildings import (
    buildExitingFieldWithRaiseException,
    buildNewVillageBuildingsWithRaiseException)
from village.types import IndoorBuildingType, Production
from village.villages import CurrentVillageAnalazer
from village.visitors import BuildFieldExceptionVisitor


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
            # Координаты деревни
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
                buildExitingFieldWithRaiseException(self.__browser) 
            else:
                # Строим новое здания из окно выбора строений
                buildNewVillageBuildingsWithRaiseException(self.__browser, self.__type, name)

        except BuildFieldException as err: 
            err.accept(BuildFieldExceptionVisitor())


# Строит ресурсное поле
class AbstractProductionFieldCommand(AbstractCommand):
    def __init__(self, type: Production, vilX: int, vilY: int): 
        super(AbstractProductionFieldCommand, self).__init__() 
        self._type: Production = type 
        self._browser = Context.browser

        self.__open_vil_command: AbstractCommand = OpenVillageCommand(vilX, vilY)
        self.__open_resources_command: AbstractCommand = OpenVillageResourcesCommand()

    def execute(self):
        self.__open_vil_command.execute()
        self.__open_resources_command.execute()
        self.__buildField()

    def __buildField(self):
        try:
            # Находим нужное поле
            field = self.__getField()
            # Открываем окно строительства поля
            field.click()
            # Строим в окне строительства
            buildExitingFieldWithRaiseException(self._browser)
        except BuildFieldException as err:
            err.accept(BuildFieldExceptionVisitor())

    def __getField(self):
        selector = self._getFieldSelector()
        elem = BaseElement(self._browser, selector)
        return elem.getElement()

    # Получить селектор для ресурсного поля
    @abstractmethod
    def _getFieldSelector(self) -> AbstractSelector:
        pass


# Строит ресурсное поле по указанному уровню
class BuildProductionFieldCommand(AbstractProductionFieldCommand): 
    def __init__(self, type: Production, lvl: int, vilX: int, vilY: int): 
        super(BuildProductionFieldCommand, self).__init__(type, vilX, vilY) 
        self.__lvl: int = lvl

    def _getFieldSelector(self) -> AbstractSelector:
        fieldLevel = self.__lvl
        return ProductionFieldSelector(self._browser, self._type, fieldLevel)


# Строит ресурсное поле с минимальным уровнем
class BuildProductionFieldWithSmallLevelCommand(AbstractProductionFieldCommand):
    def __init__(self, type: Production, vilX: int, vilY: int): 
        super(BuildProductionFieldWithSmallLevelCommand, self).__init__(type, vilX, vilY) 

    def _getFieldSelector(self) -> AbstractSelector:
        return ProductionFieldWithSmallLevelSelector(self._browser, self._type)


# Команда автоматического строительства ресурсного поля
class AutoBuildProductionFieldCommand(AbstractCommand):
    def __init__(self, vilX: int, vilY: int): 
        super(AutoBuildProductionFieldCommand, self).__init__() 
        self.__coordX = vilX
        self.__coordY = vilY
        self.__browser = Context.browser
        self.__open_vil_command: AbstractCommand = OpenVillageCommand(vilX, vilY)
        self.__open_resources_command: AbstractCommand = OpenVillageResourcesCommand()
        self.__analizer = CurrentVillageAnalazer(self.__browser)

    def execute(self):
        # открываем выбранную деревню
        self.__open_vil_command.execute()
        # Открываем вкладку ресурсов деревни
        self.__open_resources_command.execute()

        if (self.__analizer.isFieldBuilding()):
            # Ищем тип ресурсного поля, которое надо построить
            buildFieldType: Production = self.__analizer.getNextBuildFieldType()

            # Строительство ресурсного поля
            buildCommand: AbstractCommand = BuildProductionFieldWithSmallLevelCommand(
                buildFieldType, self.__coordX, self.__coordY
            )
            buildCommand.execute()
        else:
            raise BuildFieldException('Уже идёт строительство здания', BuildFieldExceptionType.ALREADY_BUILD)
