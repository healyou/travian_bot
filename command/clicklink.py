from .abstract import AbstractCommand

class ClickLinkCommand(AbstractCommand):

    def __init__(self, web_element):
        super(ClickLinkCommand, self).__init__(web_element)

    def execute(self):
        self.web_element.click()
