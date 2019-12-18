from abc import abstractmethod
from selenium.webdriver.remote import webelement
import json
from command.commands import CompositeCommand
from element.elements import *
from selector.selectors import *
from command.creator.dictionary import CommandsDictResolver, RootDictElement, CommandDictElement


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


# Создание команды из json файла с добавлением значений во время выполнения
# в json файле в значении параметра будет {code:value_code} и вместо данного значения
# будет подставлен текст из параметра values: dict (value_code/value)
class InsertValuesJsonCommandCreator(JsonCommandCreator):
    def __init__(self, browser, file_path, values: dict):
        super(JsonCommandCreator, self).__init__(browser)
        self.file_path = file_path
        self.values = values

    def configure_dictionary(self):
        f = open(self.file_path, 'r')

        fileData = f.read()
        replacedData = self.replaceDataValues(fileData)

        dict = json.loads(replacedData)
        return dict

    # Установка новых значений в словарь команды
    def replaceDataValues(self, str: str):
        replaceStr = str
        for key, value in self.values.items():
            # {code:value_code} in str value for dict (value_code/value)
            containValueCode = "{code:%s}" % key
            replaceStr = replaceStr.replace(containValueCode, value)
        return replaceStr