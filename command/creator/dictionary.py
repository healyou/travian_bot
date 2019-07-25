from enum import Enum
from abc import abstractmethod
from command.commands import *
from element.elements import *
from selector.selectors import *


class RootDictElement(Enum):
    COMMANDS = 'commands'


class CommandDictElement(Enum):
    WEB_ELEMENT = 'web_element'
    TYPE = 'type'
    VALUE = 'value'


class WebElementDict(Enum):
    TYPE = 'type'
    VALUE = 'value'


class WebElementType(Enum):
    CSS = 'css'
    ID = 'id'
    WAIT_ID = 'wait_id'


class CommandType(Enum):
    TEXT = 'text'
    CLICK = 'click'


class AbstractDictResolver(object):
    def __init__(self, dict):
        super(AbstractDictResolver, self).__init__()
        self.dict = dict

    @abstractmethod
    def create_item(self):
        pass


class CommandsDictResolver(AbstractDictResolver):
    def __init__(self, browser, dict):
        super(CommandsDictResolver, self).__init__(dict)
        self.browser = browser

    def create_item(self):
        commands = []
        for command_dict in self.dict[RootDictElement.COMMANDS.value]:
            value = command_dict[CommandDictElement.VALUE.value]
            type = command_dict[CommandDictElement.TYPE.value]
            web_element_dict = command_dict[CommandDictElement.WEB_ELEMENT.value]
            
            web_el_res = DictWebElementResolver(self.browser, web_element_dict)
            web_element = web_el_res.create_item()

            command = {
                CommandType.CLICK.value: ClickLinkCommand(web_element),
                CommandType.TEXT.value: SetTextCommand(web_element, text=value)
            }[type]

            commands.append(command)
        return commands


class DictWebElementResolver(AbstractDictResolver):
    def __init__(self, browser, dict):
        super(DictWebElementResolver, self).__init__(dict)
        self.browser = browser

    def create_item(self):
        value = self.dict[WebElementDict.VALUE.value]
        type = self.dict[WebElementDict.TYPE.value]

        selector = {
            WebElementType.ID.value: IdSelector(self.browser, value),
            WebElementType.CSS.value: CssSelector(self.browser, value),
            WebElementType.WAIT_ID.value: WaitByIdSelector(self.browser, value)
        }[type]

        return BaseElement(self.browser, selector)