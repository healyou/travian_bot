from abc import abstractmethod
from selenium.webdriver.remote import webelement
from element.elements import AbstractWebElement


class AbstractCommand(object):

    @abstractmethod
    def execute(self):
        pass


class CompositeCommand(AbstractCommand):

    def __init__(self, commands):
        super(CompositeCommand, self).__init__()
        self.commands = commands

    @abstractmethod
    def execute(self):
        for command in self.commands:
            command.execute()


class WebElementCommand(AbstractCommand):

    def __init__(self, web_element: AbstractWebElement):
        super(WebElementCommand, self).__init__()
        self.web_element = web_element


class ClickLinkCommand(WebElementCommand):

    def __init__(self, web_element: AbstractWebElement):
        super(ClickLinkCommand, self).__init__(web_element)

    def execute(self):
        element = self.web_element.getElement()
        element.click()


class SetTextCommand(WebElementCommand):

    def __init__(self, web_element: AbstractWebElement, text):
        super(SetTextCommand, self).__init__(web_element)
        self.text = text

    def execute(self):
        element = self.web_element.getElement()
        element.click()
        element.clear()
        element.send_keys(self.text)


class FactoryCommand(CompositeCommand):

    def __init__(self, factory):
        super(FactoryCommand, self).__init__(factory.createCommand())