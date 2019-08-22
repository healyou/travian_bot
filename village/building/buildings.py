import re
import time
from abc import abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from command.commands import AbstractCommand, LamdbaCommand
from element.elements import BaseElement
from selector.selectors import IdSelector
from utils.context import Context
from village.types import IndoorBuildingType, Production
from village.visitors import (BuildButtonNewIndoorVisitor,
                              BuildFieldExceptionVisitor,
                              ProductionFieldSearchNameVisitor)


def convert_str_to_int(s) -> int:
    utf = s.encode('ascii', 'ignore').decode('UTF-8')
    numStr = utf.replace(' ', '')
    return int(numStr)

def getStockBarParameter(browser, componentId) -> int:
    selector = IdSelector(browser, componentId)
    elem = BaseElement(browser, selector)
    web_elem = elem.getElement()
    return convert_str_to_int(web_elem.text)

# Строит здание через страницу увеличения уровня здания
def buildExitingFieldWithRaiseException(browser):
    # start Проверяем необходимость строительства склада или амбара
    warehouse = getStockBarParameter(browser, 'stockBarWarehouse')
    granary = getStockBarParameter(browser, 'stockBarGranary')

    build_resources_items = browser.find_elements_by_css_selector(
        'div#contract > div > div.resource'
    )
    wood_count = convert_str_to_int(build_resources_items[0].text)
    clay_count = convert_str_to_int(build_resources_items[1].text)
    iron_count = convert_str_to_int(build_resources_items[2].text)
    corn_count = convert_str_to_int(build_resources_items[3].text)

    max_resource = int(warehouse * 0.1)
    if (wood_count >= max_resource or 
        clay_count >= max_resource or 
        iron_count >= max_resource):
        print ('Необходимо строить склад')
    elif (corn_count >= int(granary * 0.1)):
        print ('Необходимо строить амбар')
    # TODO - надо добавлять параметр для создания задачи строительства амбара или склада
    # end

    field_title = browser.find_element_by_css_selector('.contentContainer > .build > .titleInHeader')
    name: str = field_title.text

    print ('Попытка построить ' + name)
    error_message = None

    # Ошибки строительства
    try:
        field = browser.find_element_by_css_selector('div.errorMessage')
        error_message = field.text
    except NoSuchElementException:
        # Если элемента нет - ошибок строительства нет
        pass

    # Ошибка апргейда здания
    if (error_message is None):
        try:
            field = browser.find_element_by_css_selector('div.upgradeBlocked > div.errorMessage')
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
            field = browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button.green.build')
            print ('Строительство: ' + name)
            # field.click()
        except NoSuchElementException:
            raise BuildFieldException('Кнопка строительства недоступна', BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE)


def buildNewVillageBuildingsWithRaiseException(browser, type: IndoorBuildingType, name: str):
    try:
        building_name = type.displayName
        visitor = BuildButtonNewIndoorVisitor(browser, building_name)
        build_button = type.newBuildType.accept(visitor)
        print ('Строим ' + building_name)
        build_button.click()
    except NoSuchElementException as err:
        raise BuildFieldException('Кнопка строительства недоступна', BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE)
