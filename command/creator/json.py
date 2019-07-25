from .factory import DictionaryCommandCreator
import json

class JsonCommandCreator(DictionaryCommandCreator):
    def __init__(self, browser, file_path):
        super(JsonCommandCreator, self).__init__()
        self.browser = browser
        self.file_path = file_path

    def configure_dictionary(self):
        f = open(self.file_path, 'r')
        return json.load(f)