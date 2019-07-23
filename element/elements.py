from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import abstractmethod
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

class WebElement(object):
    WAIT_SECONDS = 10

    def __init__(self, browser, selector):
        self.browser = browser
        self.selector = selector
        self.first_search = True
        self.element = None

    def get_element(self):
        if (self.first_search == True):
            self.element = self.selector.find_element()
            self.first_search = False
        return self.element
    
    @abstractmethod
    def click(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def send_keys(self, text):
        pass

class BaseElement(WebElement):
    def __init__(self, browser, selector):
        super(BaseElement, self).__init__(browser, selector)

    def click(self):
        self.get_element().click()

    def clear(self):
        self.get_element().clear()

    def send_keys(self, text):
        self.get_element().send_keys(text)
