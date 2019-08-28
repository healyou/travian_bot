import re
from abc import abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from datetime import datetime, timedelta

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from command.commands import AbstractCommand
from command.creator.factory import JsonCommandCreator
from element.elements import BaseElement
from selector.selectors import (AbstractSelector, IdSelector,
                                IndoorBuildingSelector,
                                ProductionFieldSelector,
                                ProductionFieldWithSmallLevelSelector)
from utils.context import Context
from utils.util import convert_str_with_one_number_to_int as toInt
from village.types import IndoorBuildingType, Production
from village.villages import CurrentVillageAnalazer
from village.visitors import (BuildButtonNewIndoorVisitor,
                              BuildFieldExceptionVisitor,
                              ProductionFieldSearchNameVisitor)
from command.queue.properties import VillageProperties


# Команда, которая имеет доступ к свойствам деревни (доп. информация для создания задач)
class AbstractVillageCommand(AbstractCommand):
    def __init__(self, coordX, coordY):
        super(AbstractVillageCommand, self).__init__()
        self._coordX = coordX
        self._coordY = coordY
        self._prop: VillageProperties = VillageProperties(coordX, coordY)

    @abstractmethod
    def execute(self):
        pass


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


# Строит здание через страницу увеличения уровня здания
class BuildExitingFieldCommand(AbstractCommand):
    def __init__(self, prop: VillageProperties): 
        super(BuildExitingFieldCommand, self).__init__() 
        self.__browser = Context.browser
        self.__prop: VillageProperties = prop

    def execute(self):
        # start Проверяем необходимость строительства склада или амбара
        warehouse = self.__getStockBarParameter('stockBarWarehouse')
        granary = self.__getStockBarParameter('stockBarGranary')

        build_resources_items = self.__browser.find_elements_by_css_selector(
            'div#contract > div > div.resource'
        )
        wood_count = self.__convert_str_to_int(build_resources_items[0].text)
        clay_count = self.__convert_str_to_int(build_resources_items[1].text)
        iron_count = self.__convert_str_to_int(build_resources_items[2].text)
        corn_count = self.__convert_str_to_int(build_resources_items[3].text)

        max_resource = int(warehouse * 0.1)
        if (wood_count >= max_resource or 
            clay_count >= max_resource or 
            iron_count >= max_resource):
            self.__prop.setNeedBuildStock()
        elif (corn_count >= int(granary * 0.1)):
            self.__prop.setNeedBuildGranary()
        # end

        field_title = self.__browser.find_element_by_css_selector('.contentContainer > .build > .titleInHeader')
        name: str = field_title.text

        print ('Попытка построить ' + name)
        error_message = None

        # Ошибки строительства
        try:
            field = self.__browser.find_element_by_css_selector('div.errorMessage')
            error_message = field.text
        except NoSuchElementException:
            # Если элемента нет - ошибок строительства нет
            pass

        # Ошибка апргейда здания
        if (error_message is None):
            try:
                field = self.__browser.find_element_by_css_selector('div.upgradeBlocked > div.errorMessage')
                error_message = field.text
            except NoSuchElementException:
                pass

        # Обработка ошибок
        if (error_message is not None):
            if ('Недостаток продовольствия: развивайте фермы' in error_message):
                raise BuildFieldException(error_message, BuildFieldExceptionType.NOT_ENOUGH_FOOD)
            elif ('Недостаточна вместимость' in error_message):
                if ('Недостаточна вместимость склада' in error_message):
                    raise BuildFieldException(error_message, BuildFieldExceptionType.INSUFFICIENT_STOCK_CAPACITY)
                elif ('Недостаточна вместимость амбара' in error_message):
                    raise BuildFieldException(error_message, BuildFieldExceptionType.INSUFFICIENT_GRANARY_CAPACITY)
                else:
                    raise BuildFieldException(error_message, BuildFieldExceptionType.INSUFFICIENT_ALL_CAPACITY)
            elif ('Достаточно ресурсов' in error_message):
                raise BuildFieldException(error_message, BuildFieldExceptionType.NOT_ENOUGH_RESOURCES)
            elif (not error_message):
                raise BuildFieldException(error_message, BuildFieldExceptionType.UNKNOWN_ERROR)
        else:
            try:
                field = self.__browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button.green.build')
                print ('Строительство: ' + name)
                # field.click()
            except NoSuchElementException:
                raise BuildFieldException('Кнопка строительства недоступна', BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE)

    def __convert_str_to_int(self, s) -> int:
        utf = s.encode('ascii', 'ignore').decode('UTF-8')
        numStr = utf.replace(' ', '')
        return int(numStr)

    def __getStockBarParameter(self, componentId) -> int:
        selector = IdSelector(self.__browser, componentId)
        elem = BaseElement(self.__browser, selector)
        web_elem = elem.getElement()
        return self.__convert_str_to_int(web_elem.text)


# Строит новое здание
class BuildNewVillageBuildings(AbstractCommand):
    def __init__(self): 
        super(BuildNewVillageBuildings, self).__init__() 
        self.__browser = Context.browser

    def execute(self):
        try:
            building_name = type.displayName
            visitor = BuildButtonNewIndoorVisitor(self.__browser, building_name)
            build_button = type.newBuildType.accept(visitor)
            print ('Строим ' + building_name)
            build_button.click()
        except NoSuchElementException as err:
            raise BuildFieldException('Кнопка строительства недоступна', BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE)


class BuildVillageBuildingCommand(AbstractVillageCommand): 
    def __init__(self, type: IndoorBuildingType, lvl: int, vilX: int, vilY: int): 
        super(BuildVillageBuildingCommand, self).__init__(vilX, vilY) 
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

            build_command: AbstractCommand = None
            if (selector.isExitingBuilding()):
                # Увеличиваем уровень здания
                build_command = BuildExitingFieldCommand(self._prop)
            else:
                # Строим новое здания из окно выбора строений
                build_command = BuildNewVillageBuildings()
            build_command.execute()

        except BuildFieldException as err: 
            err.accept(BuildFieldExceptionVisitor())


# Строит ресурсное поле
class AbstractProductionFieldCommand(AbstractVillageCommand):
    def __init__(self, type: Production, vilX: int, vilY: int): 
        super(AbstractProductionFieldCommand, self).__init__(vilX, vilY) 
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
            BuildExitingFieldCommand(self._prop).execute()
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
class AutoBuildProductionFieldCommand(AbstractVillageCommand):
    def __init__(self, vilX: int, vilY: int): 
        super(AutoBuildProductionFieldCommand, self).__init__(vilX, vilY)
        self.__browser = Context.browser
        self.__open_vil_command: AbstractCommand = OpenVillageCommand(vilX, vilY)
        self.__open_resources_command: AbstractCommand = OpenVillageResourcesCommand()
        self.__analizer = CurrentVillageAnalazer(self.__browser)

    def execute(self):
        # открываем выбранную деревню
        self.__open_vil_command.execute()
        # Открываем вкладку ресурсов деревни
        self.__open_resources_command.execute()

        if (not self.__analizer.isFieldBuilding()):
            # Ищем тип ресурсного поля, которое надо построить
            buildFieldType: Production = self.__analizer.getNextBuildFieldType()

            # Строительство ресурсного поля
            buildCommand: AbstractCommand = BuildProductionFieldWithSmallLevelCommand(
                buildFieldType, self._coordX, self._coordY
            )
            buildCommand.execute()
        else:
            # Устанавливаем время для след. строительства данной деревни
            time_to_build_field: int = self.__analizer.getSecondsToEndBuildFields()
            next_build_datetime = datetime.now() + timedelta(seconds=time_to_build_field)
            self._prop.setNextBuildDatetime(next_build_datetime)

            # TODO - надо try catch в месте выполнения команд
            # raise BuildFieldException('Уже идёт строительство здания', BuildFieldExceptionType.ALREADY_BUILD)
