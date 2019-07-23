from abc import abstractmethod
from selenium.webdriver.remote import webelement
import json
from command.settext import SetTextCommand
from command.clicklink import ClickLinkCommand
from element.elements import *
from selector.selectors import *

class AbstractFactory(object):

    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def create_commands(self):
        pass

class JsonFactory(AbstractFactory):

    def __init__(self, browser, file_path):
        super(JsonFactory, self).__init__(file_path)
        self.browser = browser

    def create_commands(self):
        commands = []
        with open(self.file_path, 'r') as f:
            json_data = json.load(f)
            json_commands = json_data['commands']
            for json_command in json_commands:
                web_element = json_command['web_element']
                value = json_command['value']

                web_el_value = web_element['value']
                if (web_element['type'] == 'id'):
                    s = IdSelector(self.browser, web_el_value)
                    e = BaseElement(self.browser, s)
                elif (web_element['type'] == 'wait_id'):
                    s = WaitByIdSelector(self.browser, web_el_value)
                    e = BaseElement(self.browser, s)
                elif (web_element['type'] == 'css'):
                    s = CssSelector(self.browser, web_el_value)
                    e = BaseElement(self.browser, s)

                if (json_command['type'] == 'text'):
                    commands.append(SetTextCommand(e, text=value))
                elif (json_command['type'] == 'click'):
                    commands.append(ClickLinkCommand(e))
        return commands

                