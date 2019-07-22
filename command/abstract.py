from abc import abstractmethod
from selenium.webdriver.remote import webelement

class AbstractCommand(object):

    def __init__(self, web_element):
        self.web_element = web_element

    @abstractmethod
    def execute(self):
        pass