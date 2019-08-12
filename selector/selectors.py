from abc import abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from village.types import Production


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


class ProductionFieldSelector(AbstractSelector):
    def __init__(self, browser, type: Production, lvl: int):
        super(ProductionFieldSelector, self).__init__(browser)
        self._type: Production = type
        self._lvl: int = lvl

    def findElement(self):
        return self.__getFirstFieldForSelectedType()

    # Получить первое поле по указанному типу и уровню
    def __getFirstFieldForSelectedType(self):
        name_for_search = self.__getFieldName()
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

    def __getFieldName(self) -> str:
        lvl_str = str(self._lvl)
        return {
            Production.WOOD: 'Лесопилка Уровень ' + lvl_str,
            Production.IRON: 'Железный рудник Уровень ' + lvl_str,
            Production.CLAY: 'Глиняный карьер Уровень ' + lvl_str,
            Production.CORN: 'Ферма Уровень ' + lvl_str,
        }[self._type]