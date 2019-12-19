from command.creator.factory import JsonCommandCreator, InsertValuesJsonCommandCreator
from selenium.webdriver import Chrome
from selenium.webdriver import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selector.selectors import HasPresentElementSelector, CssSelector, WaitByCssSelector


def create_browser():
    return Chrome(executable_path='install/chromedriver.exe')

def open_travian(browser, serverUrl: str):
    browser.get(serverUrl)
    WebDriverWait(browser, 5).until(
        method=EC.presence_of_element_located((By.CLASS_NAME, 'outerLoginBox')), 
        message='Page not load exception'
    )

def login_to_account(browser, login: str, psw: str):
    # TODO - объединить открытие страницы логина и сам ввод в одну команду для проверки ошибок
    insertValuesDict = {
		"login" : login,
		"psw" : psw
	}
    creator = InsertValuesJsonCommandCreator(browser, 'files/travian/login.json', insertValuesDict)
    command = creator.createCommand()
    # TODO - логин не проверяет правильность ввода данных
    command.execute()

    # TODO - выделить в отдельное место проверку логина
    hasPresentCaptcha = HasPresentElementSelector(browser, CssSelector(browser, 'th.captcha'))
    if hasPresentCaptcha.hasPresentElement():
        raise Exception('Present captcha for login')
    else:
        errorElemSelector = WaitByCssSelector(browser, 'div.error.LTR')
        errorElement = errorElemSelector.findElement()
        errorText = errorElement.text


def open_resources(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_resources.json')
    command = creator.createCommand()
    command.execute()


def open_village(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_village.json')
    command = creator.createCommand()
    command.execute()
