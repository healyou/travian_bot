from abc import abstractmethod
import utils.util as util
from element.elements import BaseElement
from selector.selectors import *
from enum import Enum


class AbstractVillage(object):
    def __init__(self):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def analyze(self):
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

    @abstractmethod
    def build(self):
        pass

    def get_next_build_field_type(self):
        build_prod_types = dict((k,self.production[k]) for k in getBuildProductions() if k in self.production)
        import operator
        sorted_types = sorted(build_prod_types.items(), key=operator.itemgetter(1))
        return sorted_types[0][0]

    def analyze(self):
        self.warehouse = self.getStockBarParameter('stockBarWarehouse')
        self.granary = self.getStockBarParameter('stockBarGranary')
        self.production = self.getProductionParameters()

    def getStockBarParameter(self, componentId):
        selector = IdSelector(self.browser, componentId)
        elem = BaseElement(self.browser, selector)
        web_elem = elem.get_element()
        return util.convert_str_to_int(web_elem.text)

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
            production[type] = util.convert_str_to_int(text)

        print (production)
        return production