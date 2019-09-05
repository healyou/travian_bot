from command.creator.factory import JsonCommandCreator
from selenium.webdriver import Chrome


def create_browser():
    return Chrome(executable_path='install/chromedriver.exe')

def open_travian(browser):
    browser.get('https://ts3.travian.ru')

def login_to_account(browser):
    creator = JsonCommandCreator(browser, 'files/travian/login.json')
    command = creator.createCommand()
    command.execute()


def open_resources(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_resources.json')
    command = creator.createCommand()
    command.execute()


def open_village(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_village.json')
    command = creator.createCommand()
    command.execute()
