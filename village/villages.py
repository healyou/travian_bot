from abc import abstractmethod
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


class Village(AbstractVillage):
    def __init__(self, browser):
        super(Village, self).__init__()
        self.browser = browser

        self.name = 'unknown'
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

    @abstractmethod
    def analyze(self):
        self.warehouse = self.getStockBarParameter('stockBarWarehouse')
        self.granary = self.getStockBarParameter('stockBarGranary')
        self.production = self.getProductionParameters()

    # todo - сделать рефактор
    def getStockBarParameter(self, componentId):
        selector = IdSelector(self.browser, componentId)
        elem = BaseElement(self.browser, selector)
        web_elem = elem.get_element()
        text = web_elem.text
        value = text.encode('ascii', 'ignore').decode('UTF-8').replace(' ', '');
        int_value = int(value)
        return int_value

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
            value = text.encode('ascii', 'ignore').decode('UTF-8').replace(' ', '');
            production[type] = int(value)

        return production