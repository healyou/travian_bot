from command.creator.factory import JsonCommandCreator, InsertValuesJsonCommandCreator
from typing import List
from selenium.webdriver import Chrome
from selenium.webdriver import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from command.commands import AbstractCommand
from selector.selectors import HasPresentElementSelector, CssSelector, WaitByCssSelector, HasPresentOneOfElements, AbstractSelector, WaitByClassNameSelector


def create_browser():
    return Chrome(executable_path='install/chromedriver.exe')

def login_to_account(browser, serverUrl: str, login: str, psw: str):
    LoginToAccountCommand(browser, serverUrl, login, psw).execute()

def open_resources(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_resources.json')
    command = creator.createCommand()
    command.execute()

def open_village(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_village.json')
    command = creator.createCommand()
    command.execute()


# TODO - возможно надо куда-то перенести
class LoginToAccountCommand(AbstractCommand):
    def __init__(self, browser, serverUrl: str, login: str, psw: str):
        super(LoginToAccountCommand, self).__init__()
        self.browser = browser
        self.serverUrl = serverUrl;
        self.login = login
        self.psw = psw

    def execute(self):
        self.openTravianLoginPage()
        self.enterCridentional()
        self.validateLogin()  

    def openTravianLoginPage(self):
        self.browser.get(self.serverUrl)
        pageLoadSelector = HasPresentElementSelector(self.browser, WaitByClassNameSelector(self.browser, 'outerLoginBox'))
        if (not pageLoadSelector.hasPresentElement()):
            raise Exception('Login page not load')

    def enterCridentional(self):
        insertValuesDict = {
            "login" : self.login,
            "psw" : self.psw
        }
        creator = InsertValuesJsonCommandCreator(self.browser, 'files/travian/login.json', insertValuesDict)
        command = creator.createCommand()
        command.execute()

    def validateLogin(self):
        selectors = [CssSelector(self.browser, 'th.captcha'), CssSelector(self.browser, 'div.error.LTR')] # type: List[AbstractSelector]
        hasPresentErrorComponents = HasPresentOneOfElements(self.browser, selectors)
        if (hasPresentErrorComponents.hasPresentElement()):
            raise Exception('Login error')
