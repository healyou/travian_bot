from .abstract import AbstractCommand

class SetTextCommand(AbstractCommand):

    def __init__(self, web_element, text):
        super(SetTextCommand, self).__init__(web_element)
        self.text = text

    def execute(self):
        self.web_element.click()
        self.web_element.clear()
        self.web_element.send_keys(self.text)