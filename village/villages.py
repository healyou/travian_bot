from abc import abstractmethod
from element.elements import BaseElement
from selector.selectors import *
from enum import Enum
from utils.util import *
from utils.context import Context
from selenium.common.exceptions import NoSuchElementException
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
import re
from village.visitors import BuildFieldExceptionVisitor
import operator


class AbstractVillage(object):
    def __init__(self):
        pass

    @abstractmethod
    def analyzeProperties(self):
        pass

    @abstractmethod
    def isFieldBuilding(self):
        pass

    @abstractmethod
    def getNextBuildFieldType(self):
        pass

    @abstractmethod
    def tryToBuildField(self, field_type):
        pass

    @abstractmethod
    def build(self, name_for_search):
        pass


class Production(Enum):
    WOOD = 'wood'
    CLAY = 'clay'
    IRON = 'iron'
    CORN = 'corn'

def getBuildProductionTypes():
    return {
        Production.WOOD, 
        Production.CLAY, 
        Production.IRON,
        Production.CORN
    }


class Village(AbstractVillage):
    def __init__(self, browser, name):
        super(Village, self).__init__()
        self.browser = browser
        self.name = name
        self.warehouse = 0
        self.granary = 0
        self.production = {
            Production.WOOD: 0,
            Production.CLAY: 0,
            Production.IRON: 0,
            Production.CORN: 0
        }
        self.analyzeProperties()

    # Постройка поля 
    def run(self):
        self.build()
        # if (self.isFieldBuilding()):
        #     self.build()
        # else:
        #     print ('Идёт строительство здани(я/й)')
        #     print ('Неудачная попытка построить здание')

    def build(self):
        try:
            type = self.getNextBuildFieldType()
            self.tryToBuildField(type)
        except BuildFieldException as err:
            err.accept(BuildFieldExceptionVisitor())
                

    def getFieldNameByBuildingType(self, type: Production) -> str:
        return {
            Production.WOOD: 'Лесопилка Уровень',
            Production.IRON: 'Железный рудник Уровень',
            Production.CLAY: 'Глиняный карьер Уровень',
            Production.CORN: 'Ферма Уровень'
        }[type]

    def tryToBuildField(self, type: Production):
        # Список полей указанного типа
        search_fields = self.getFieldsForSelectedType(type)
        # Определяем поле с наименьшим уровнем для строительства
        field = self.getFieldWithSmallLevel(search_fields)
        # Собственно строим здание
        self.buildFieldWithRaiseException(field)

    def buildFieldWithRaiseException(self, field):
        name = field.get_attribute('alt')
        print ('Попытка построить здание ' + name)
        field.click()
        error_message = ''
        try:
            field = self.browser.find_element_by_css_selector('div.errorMessage > span')
            error_message = field.text
        except NoSuchElementException:
            pass

        if ('Недостаток продовольствия: развивайте фермы' in error_message):
            raise BuildFieldException(error_message, BuildFieldExceptionType.NOT_ENOUGH_FOOD, self)
        else:
            try:
                field = self.browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button.green.build')
                print ('Строительство поля: ' + name)
                field.click()
            except NoSuchElementException:
                raise BuildFieldException('Кнопка строительства недоступна', BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE, self)

    # Получить элементы всех полей по заданному типу
    def getFieldsForSelectedType(self, type: Production):
        name_for_search = self.getFieldNameByBuildingType(type)
        # Информация обо всех полях деревни
        fields = self.browser.find_elements_by_css_selector('div > map#rx > area[shape=\'circle\']')
        search_fields = []
        for field in fields:
            name = field.get_attribute('alt')
            if (name_for_search in name):
                search_fields.append(field)
        return search_fields

    # TODO сделать приватные переменные и протектные в питоне
    # Получить поле с самым маленьким уровнем
    def getFieldWithSmallLevel(self, search_fields):
        min_lvl_field = None
        min_lvl = None
        for field in search_fields:
            name = field.get_attribute('alt')
            lvl = int(re.findall("\d+", name)[0])
            if (min_lvl is None or min_lvl > lvl):
                min_lvl = lvl
                min_lvl_field = field
        return min_lvl_field

    # Строится ли уже какое-то здание
    def isFieldBuilding(self):
        # Текущее строительство и время до его завершения
        fields = self.browser.find_elements_by_css_selector('div[class=\'buildDuration\'] > span')
        if (len(fields) > 0):
            for field in fields:
                print ('Здание ещё строится ' + field.get_attribute('value') + ' сек')
            return False
        else:
            return True

    # Получить тип поля с самым маленьким уровнем производства
    def getNextBuildFieldType(self) -> Production:
        build_prod_types = dict((k,self.production[k]) for k in getBuildProductionTypes() if k in self.production)

        # зерно считаем на 50% больше, т.к. его много ненадо
        corn_prod = build_prod_types[Production.CORN]
        build_prod_types[Production.CORN] = int(corn_prod * 1.5)

        sorted_types = sorted(build_prod_types.items(), key=operator.itemgetter(1))
        return sorted_types[0][0]

    def analyzeProperties(self):
        self.warehouse = self.getStockBarParameter('stockBarWarehouse')
        self.granary = self.getStockBarParameter('stockBarGranary')
        self.production = self.getProductionParameters()

    def getStockBarParameter(self, componentId):
        selector = IdSelector(self.browser, componentId)
        elem = BaseElement(self.browser, selector)
        web_elem = elem.getElement()
        return self.convert_str_to_int(web_elem.text)

    def getProductionParameters(self):
        production = {
            Production.WOOD: 0,
            Production.CLAY: 0,
            Production.IRON: 0,
            Production.CORN: 0
        }
        css = '.boxes-contents.cf > table > tbody > tr > .res'
        elems = self.browser.find_elements_by_css_selector(css)
        for elem in elems:
            text = elem.text
            type = ''
            if ('Древесина' in text):
                type = Production.WOOD
            elif ('Глина' in text):
                type = Production.CLAY
            elif ('Железо' in text):
                type = Production.IRON
            elif ('Зерно' in text):
                type = Production.CORN
            
            parent = elem.find_element_by_xpath('..')
            num_elem = parent.find_element_by_css_selector('.num')
            text = num_elem.text
            production[type] = self.convert_str_to_int(text)

        print (production)
        return production

    def convert_str_to_int(self, s):
        utf = s.encode('ascii', 'ignore').decode('UTF-8')
        numStr = utf.replace(' ', '')
        return int(numStr)