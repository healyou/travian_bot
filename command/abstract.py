from abc import abstractmethod
from selenium.webdriver.remote import webelement

class AbstractCommand(object):

    @abstractmethod
    def execute(self):
        pass