import operator
from abc import abstractmethod

from element.elements import BaseElement
from selector.selectors import IdSelector
from utils.context import Context

from .types import IndoorBuildingType, Production


class AbstractVillage(object):
    def __init__(self):
        pass

    @abstractmethod
    def getNextBuildFieldType(self) -> Production:
        pass


class CurrentVillageAnalazer(AbstractVillage):
    def __init__(self, browser):
        super(CurrentVillageAnalazer, self).__init__()
        self.browser = browser
        self.warehouse = 0
        self.granary = 0
        self.production = {
            Production.WOOD: 0,
            Production.CLAY: 0,
            Production.IRON: 0,
            Production.CORN: 0
        }

    # Получить тип поля с самым маленьким уровнем производства
    def getNextBuildFieldType(self) -> Production:
        self.__analyzeProperties()
        return self.__searchNextBuildResourceType()

    def __searchNextBuildResourceType(self) -> Production:
        build_prod_types = dict((k,self.production[k]) for k in Production if k in self.production)

        # зерно считаем на 50% больше, т.к. его много ненадо
        corn_prod = build_prod_types[Production.CORN]
        build_prod_types[Production.CORN] = int(corn_prod * 1.5)

        sorted_types = sorted(build_prod_types.items(), key=operator.itemgetter(1))
        return sorted_types[0][0]

    # Строится ли уже какое-то здание
    def isFieldBuilding(self) -> bool:
        # Текущее строительство и время до его завершения
        fields = self.browser.find_elements_by_css_selector('div[class=\'buildDuration\'] > span')
        if (len(fields) > 0):
            for field in fields:
                print ('Здание ещё строится ' + field.get_attribute('value') + ' сек')
            return True
        else:
            return False

    def __analyzeProperties(self):
        self.warehouse = self.__getStockBarParameter('stockBarWarehouse')
        self.granary = self.__getStockBarParameter('stockBarGranary')
        self.production = self.__getProductionParameters()

    def __getStockBarParameter(self, componentId):
        selector = IdSelector(self.browser, componentId)
        elem = BaseElement(self.browser, selector)
        web_elem = elem.getElement()
        return self.__convert_str_to_int(web_elem.text)

    def __getProductionParameters(self):
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
            production[type] = self.__convert_str_to_int(text)

        print (production)
        return production

    def __convert_str_to_int(self, s):
        utf = s.encode('ascii', 'ignore').decode('UTF-8')
        numStr = utf.replace(' ', '')
        return int(numStr)
