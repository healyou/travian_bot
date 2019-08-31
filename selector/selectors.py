import re
from abc import abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import \
    WebElement as SeleniumWebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from command.commands import AbstractCommand, LamdbaCommand
from village.types import IndoorBuildingType, Production
from village.visitors import (IndoorBuildingTypeSearchNameVisitor,
                              ProductionFieldSearchNameVisitor,
                              IsMultipleBuildFieldVisitor)


class AbstractSelector(object):
    def __init__(self, browser):
        self._browser = browser

    @abstractmethod
    def findElement(self):
        pass


class CssSelector(AbstractSelector):
    def __init__(self, browser, value):
        super(CssSelector, self).__init__(browser)
        self.value = value

    def findElement(self):
        return self._browser.find_element_by_css_selector(self.value)


class IdSelector(AbstractSelector):
    def __init__(self, browser, id):
        super(IdSelector, self).__init__(browser)
        self.id = id

    def findElement(self):
        return self._browser.find_element_by_id(self.id)


class WaitByIdSelector(AbstractSelector):
    WAIT_SECONDS = 10
    
    def __init__(self, browser, id):
        super(WaitByIdSelector, self).__init__(browser)
        self.id = id

    @abstractmethod
    def findElement(self):
        return WebDriverWait(self._browser, self.WAIT_SECONDS).until(
            EC.presence_of_element_located((By.ID, self.id))
        )


# Поиск клетки для строительства внутрю здания деревни
class IndoorBuildingSelector(AbstractSelector):
    def __init__(self, browser, type: IndoorBuildingType): 
        super(IndoorBuildingSelector, self).__init__(browser) 
        self._type: IndoorBuildingType = type
        self._exiting_building: bool = None
        self._find_item = None
    
    # Вернёт элемент, по которому можно кликнуть для перехода в окно строительства
    def findElement(self):
        self.__findFieldForSelectedType()
        return self._find_item

    def clickToElement(self):
        if (self._find_item is None):
            raise Exception('Необходимо вначале найти элемент')
        else:
            if (self._type == IndoorBuildingType.HEDGE):
                # По изгороди просто так не кликнуть
                hover = ActionChains(self._browser).move_to_element(self._find_item).click()
                hover.perform()
            else:
                # По всем другим полям клик проходит без проблем
                self._find_item.click()

    # Определяет, построен ли хоть один уровень данного здания
    def isExitingBuilding(self) -> bool:
        if (self._exiting_building is None):
            raise Exception('Необходимо вначале найти элемент')
        else:
            return self._exiting_building
    
    # Получить поле по указанному типу и уровню, на котором будем строить здание
    def __findFieldForSelectedType(self):
        browser = self._browser

        # Возможность строить несколько одинаковых зданий
        is_multiple_build_field: bool = self._type.accept(IsMultipleBuildFieldVisitor())
        
        village_map = browser.find_element_by_css_selector('div#village_map')
        elems = village_map.find_elements_by_xpath('//div[contains(@class, \'buildingSlot\') and .//div[contains(@class, \'level\')]]')

        build_clicked_field = None
        name = None
        for elem in elems:
            # hover по иконке с уровнем здания
            level_item_to_hover = elem.find_element_by_css_selector('.level')
            hover = ActionChains(browser).move_to_element(level_item_to_hover)
            hover.perform()

            build_container = elem
            
            # здесь текст основных зданий
            hover_elem_tytle = browser.find_element_by_css_selector('div.tip > div.tip-container > div.tip-contents > div.title.elementTitle')

            # Получаем текст первого уровня
            all_text = hover_elem_tytle.text
            child_elems = hover_elem_tytle.find_elements_by_xpath("./*")
            parent_text = all_text
            for child in child_elems:
                parent_text = parent_text.replace(child.text, '')

            # TODO Наводим на далеко расположенный item - почему-то без этого не всегда срабатывает hover элемента
            hover_item = browser.find_element_by_css_selector('button#heroImageButton')
            hover = ActionChains(browser).move_to_element(hover_item)
            hover.perform()

            # Находим имя компонента, который надо найти
            search_name = self._type.accept(IndoorBuildingTypeSearchNameVisitor())
            if (search_name in parent_text):
                # Если зданий может быть несколько, то при макс. уровне надо строить новое
                if (is_multiple_build_field):
                    is_max_lvl = 'maxLevel' in level_item_to_hover.get_attribute("class")
                    if (is_max_lvl):
                        print ('Найдено искомое здание с максимальным уровнем')
                        continue

                build_clicked_field = level_item_to_hover
                name = self._type.displayName
                break

        if (build_clicked_field is not None):
            print ('Найдено поле ' + name)
            self._find_item = build_clicked_field
            self._exiting_building = True
        else:
            print ('Надо строить новое здание')
            # Находим первую свободную стройплощадку
            try:
                empty_field_sel = 'div.g0 > svg.buildingShape > .hoverShapeWinter'
                first_empty_clicked_field = village_map.find_element_by_css_selector(empty_field_sel)
                self._find_item = first_empty_clicked_field
                self._exiting_building = False
            except NoSuchElementException as err:
                raise BuildFieldException('Нет места для строительства здания', BuildFieldExceptionType.NOT_ENOUGH_PLACE)


# Поиск компонента ресурсного поля
class ProductionFieldSelector(AbstractSelector):
    def __init__(self, browser, type: Production, lvl: int):
        super(ProductionFieldSelector, self).__init__(browser)
        self._type: Production = type
        self._lvl: int = lvl

    def findElement(self):
        return self.__getFirstFieldForSelectedType()

    # Получить первое поле по указанному типу и уровню
    def __getFirstFieldForSelectedType(self):
        name_for_search = self.__getFieldSearchName()
        # Информация обо всех полях деревни
        fields = self._browser.find_elements_by_css_selector('div > map#rx > area[shape=\'circle\']')
        search_fields = []
        for field in fields:
            name = field.get_attribute('alt')
            if (name_for_search in name):
                search_fields.append(field)
        if (len(search_fields) == 0):
            raise Exception('Не найдено ресурсное поле по указанным параметрам')
        else:
            return search_fields[0]

    def __getFieldSearchName(self) -> str:
        lvl_str = str(self._lvl)
        return self._type.accept(ProductionFieldSearchNameVisitor()) + ' ' + lvl_str


# Находит компонент ресурсного поля с самым маленьким уровнем
class ProductionFieldWithSmallLevelSelector(AbstractSelector):
    def __init__(self, browser, type: Production):
        super(ProductionFieldWithSmallLevelSelector, self).__init__(browser)
        self._type: Production = type

    def findElement(self):
        return self.__getFirstFieldForSelectedType()

    # Получить первое поле по указанному типу и уровню
    def __getFirstFieldForSelectedType(self):
        name_for_search = self.__getFieldSearchName()
        # Информация обо всех полях деревни
        fields = self._browser.find_elements_by_css_selector('div > map#rx > area[shape=\'circle\']')

        small_field_lvl: int = None
        small_field = None
        for field in fields:
            name_with_level = field.get_attribute('alt')

            # Поле нашего типа
            if (name_for_search in name_with_level):
                field_level: int = int(re.findall('\d+', name_with_level)[0])

                if (small_field_lvl is None or field_level < small_field_lvl):
                    small_field_lvl = field_level
                    small_field = field
        
        return small_field

    def __getFieldSearchName(self) -> str:
        return self._type.accept(ProductionFieldSearchNameVisitor())
