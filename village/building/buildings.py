from abc import abstractmethod
from village.visitors import BuildFieldExceptionVisitor
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from selenium.common.exceptions import NoSuchElementException
import re
from utils.context import Context
from village.types import Production, IndoorBuildingType
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from command.commands import AbstractCommand, LamdbaCommand
from village.visitors import ProductionFieldSearchNameVisitor, BuildButtonNewIndoorVisitor

# Строит здание через страницу увеличения уровня здания
def buildExitingFieldWithRaiseException(browser):
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
