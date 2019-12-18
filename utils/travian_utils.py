from command.creator.factory import JsonCommandCreator, InsertValuesJsonCommandCreator
from selenium.webdriver import Chrome
from selenium.webdriver import *


def create_browser():
    return Chrome(executable_path='install/chromedriver.exe')

def open_travian(browser, serverUrl: str):
    browser.get(serverUrl)

def login_to_account(browser, login: str, psw: str):
    insertValuesDict = {
		"login" : login,
		"psw" : psw
	}
    creator = InsertValuesJsonCommandCreator(browser, 'files/travian/login.json', insertValuesDict)
    command = creator.createCommand()
    # TODO - логин не проверяет правильность ввода данных
    command.execute()


def open_resources(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_resources.json')
    command = creator.createCommand()
    command.execute()


def open_village(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_village.json')
    command = creator.createCommand()
    command.execute()
