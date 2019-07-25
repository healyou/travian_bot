from abc import abstractmethod
from selenium.webdriver.remote import webelement
import json
from command.commands import *
from element.elements import *
from selector.selectors import *


class AbstractCommandCreator(object):
    @abstractmethod
    def create_command(self):
        pass


class DictionaryCommandCreator(AbstractCommandCreator):
    def __init__(self):
        super(DictionaryCommandCreator, self).__init__()

    def create_command(self):
        commands = []

        # todo надо сюда добавить анализаторы словаря
        # который будет создавать ныжные элементы
        # как организовать структуру?

        dict = self.configure_dictionary()
        json_commands = dict['commands']
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
    
        return CompositeCommand(commands)

    @abstractmethod
    def configure_dictionary(self):
        pass

                