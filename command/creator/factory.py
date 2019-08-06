from abc import abstractmethod
from selenium.webdriver.remote import webelement
import json
from command.commands import CompositeCommand
from element.elements import *
from selector.selectors import *
from command.creator.dictionary import CommandsDictResolver


class AbstractCommandCreator(object):
    @abstractmethod
    def createCommand(self):
        pass


class DictionaryCommandCreator(AbstractCommandCreator):
    def __init__(self, browser):
        super(DictionaryCommandCreator, self).__init__()
        self.browser = browser

    def createCommand(self):
        dict = self.configure_dictionary()
        resolver = CommandsDictResolver(self.browser, dict)
        commands = resolver.createItem()
        return CompositeCommand(commands)

    @abstractmethod
    def configure_dictionary(self):
        pass

                
class JsonCommandCreator(DictionaryCommandCreator):
    def __init__(self, browser, file_path):
        super(JsonCommandCreator, self).__init__(browser)
        self.file_path = file_path

    def configure_dictionary(self):
        f = open(self.file_path, 'r')
        return json.load(f)