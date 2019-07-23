from abc import abstractmethod
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement


class AbstractSelector(object):
    def __init__(self, browser):
        self.browser = browser

    @abstractmethod
    def find_element(self):
        pass


class CssSelector(AbstractSelector):
    def __init__(self, browser, value):
        super(CssSelector, self).__init__(browser)
        self.value = value

    def find_element(self):
        return self.browser.find_element_by_css_selector(self.value)


class IdSelector(AbstractSelector):
    def __init__(self, browser, id):
        super(IdSelector, self).__init__(browser)
        self.id = id

    def find_element(self):
        return self.browser.find_element_by_id(self.id)


class WaitByIdSelector(AbstractSelector):
    WAIT_SECONDS = 10
    
    def __init__(self, browser, id):
        super(WaitByIdSelector, self).__init__(browser)
        self.id = id

    @abstractmethod
    def find_element(self):
        return WebDriverWait(self.browser, self.WAIT_SECONDS).until(
            EC.presence_of_element_located((By.ID, self.id))
        )
