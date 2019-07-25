from abc import abstractmethod
from selenium.webdriver.remote import webelement

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

    def __init__(self, web_element):
        super(WebElementCommand, self).__init__()
        self.web_element = web_element


class ClickLinkCommand(WebElementCommand):

    def __init__(self, web_element):
        super(ClickLinkCommand, self).__init__(web_element)

    def execute(self):
        element = self.web_element.get_element()
        element.click()


class SetTextCommand(WebElementCommand):

    def __init__(self, web_element, text):
        super(SetTextCommand, self).__init__(web_element)
        self.text = text

    def execute(self):
        element = self.web_element.get_element()
        element.click()
        element.clear()
        element.send_keys(self.text)


class FactoryCommand(CompositeCommand):

    def __init__(self, factory):
        super(FactoryCommand, self).__init__(factory.create_commands())