from abc import abstractmethod
from element.elements import BaseElement
from selector.selectors import *
from enum import Enum
from utils.util import *
from utils.context import Context
from selenium.common.exceptions import NoSuchElementException
from exceptions.exceptions import MyException
import re


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

def getBuildProductions():
    return {
        Production.WOOD.value, 
        Production.CLAY.value, 
        Production.IRON.value
    }


class Village(AbstractVillage):
    def __init__(self, browser, name):
        super(Village, self).__init__()
        self.browser = browser
        self.name = name
        self.warehouse = 0
        self.granary = 0
        self.production = {
            Production.WOOD.value: 0,
            Production.CLAY.value: 0,
            Production.IRON.value: 0,
            Production.CORN.value: 0
        }

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
        except MyException as err:
            # TODO - туд должна быть обработка ошибок(посетитель)
            print('Ошибка строительства здания: ' + str(err))
            if (Context.buildCornOnError):
                print('Попытка построить ферму')
                # self.tryToBuildField(Production.CORN.value)

    def getFieldNameByBuildingType(self, type):
        return {
            Production.WOOD.value: 'Лесопилка Уровень',
            Production.IRON.value: 'Железный рудник Уровень',
            Production.CLAY.value: 'Глиняный карьер Уровень',
            Production.CORN.value: 'Ферма Уровень'
        }[type]

    def tryToBuildField(self, type):
        # Список полей указанного типа
        search_fields = self.getFieldsForSelectedType(type)
        # Определяем поле с наименьшим уровнем для строительства
        field = self.getFieldWithSmallLevel(search_fields)
        # Собственно строим здание
        self.buildFieldWithRaiseException(field)

    def buildFieldWithRaiseException(self, field):
        name = field.get_attribute('alt')
        # TODO надо определять поле с наименьшим уровнем для строительства и пытаться строить его
        # TODO возможны различные ошибки при строительстве здания - их надо централизовано все обрабатывать
        print ('Попытка построить здание ' + name)
        field.click()
        error_message = ''
        try:
            field = self.browser.find_element_by_css_selector('div.errorMessage > span')
            error_message = field.text
        except NoSuchElementException:
            pass

        if ('Недостаток продовольствия: развивайте фермы' in error_message):
            raise MyException(error_message)
        else:
            # TODO мб ошибка строительства другая
            try:
                field = self.browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button.green.build')
                print ('Строительство поля: ' + name)
                field.click()
            except NoSuchElementException:
                raise MyException('Кнопка строительства недоступна')

    # Получить элементы всех полей по заданному типу
    def getFieldsForSelectedType(self, type):
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

    def getNextBuildFieldType(self):
        # TODO - почему-то не те поля находит
        build_prod_types = dict((k,self.production[k]) for k in getBuildProductions() if k in self.production)
        import operator
        sorted_types = sorted(build_prod_types.items(), key=operator.itemgetter(1))
        return sorted_types[0][0]

    def analyzeProperties(self):
        self.warehouse = self.getStockBarParameter('stockBarWarehouse')
        self.granary = self.getStockBarParameter('stockBarGranary')
        self.production = self.getProductionParameters()

    def getStockBarParameter(self, componentId):
        selector = IdSelector(self.browser, componentId)
        elem = BaseElement(self.browser, selector)
        web_elem = elem.get_element()
        return self.convert_str_to_int(web_elem.text)

    def getProductionParameters(self):
        production = {
            Production.WOOD.value: 0,
            Production.CLAY.value: 0,
            Production.IRON.value: 0,
            Production.CORN.value: 0
        }
        css = '.boxes-contents.cf > table > tbody > tr > .res'
        elems = self.browser.find_elements_by_css_selector(css)
        for elem in elems:
            text = elem.text
            type = ''
            if ('Древесина' in text):
                type = Production.WOOD.value
            elif ('Глина' in text):
                type = Production.CLAY.value
            elif ('Железо' in text):
                type = Production.IRON.value
            elif ('Зерно' in text):
                type = Production.CORN.value
            
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