from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import abstractmethod
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

class WebElement(object):
    WAIT_SECONDS = 10

    def __init__(self, browser):
        self.browser = browser

    @abstractmethod
    def get_element(self):
        pass
    
    @abstractmethod
    def click(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def send_keys(self, text):
        pass

class ElementById(WebElement):
    def __init__(self, browser, id):
        super(ElementById, self).__init__(browser)
        self.id = id

    def click(self):
        self.get_element().click()

    def clear(self):
        self.get_element().clear()

    def send_keys(self, text):
        self.get_element().send_keys(text)

    def get_element(self):
        return self.browser.find_element_by_id(self.id)


class WaitWebElement(WebElement):
    def __init__(self, browser):
        super(WaitWebElement, self).__init__(browser)

    def click(self):
        self.get_element().click()

    def clear(self):
        self.get_element().clear()

    def get_element(self):
        return WebDriverWait(self.browser, self.WAIT_SECONDS).until(
            self.get_locator()
        )
    
    @abstractmethod
    def get_locator(self):
        pass


class WaitElementById(WaitWebElement):
    def __init__(self, browser, id):
        super(WaitElementById, self).__init__(browser)
        self.id = id

    def get_locator(self):
        return EC.presence_of_element_located((By.ID, self.id))
