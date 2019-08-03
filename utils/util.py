import os
from selenium.webdriver import Chrome
from command.creator.factory import *
from command.commands import FactoryCommand
from village.villages import Village


def get_absolute_file_path(cur_script_file, rel_file_path):
    script_dir = os.path.dirname(cur_script_file)
    return os.path.join(script_dir, rel_file_path)


def convert_str_to_int(s):
    utf = s.encode('ascii', 'ignore').decode('UTF-8')
    numStr = utf.replace(' ', '')
    return int(numStr)


def get_travian_command_files():
    return [
        'files/travian/login.json',
        # 'files/travian/open_village.json',
        # 'files/travian/open_map.json',
        # 'files/travian/open_resources.json'
    ]


def open_travian():
    browser = Chrome(executable_path='install/chromedriver.exe')
    browser.get('https://ts3.travian.ru')
    return browser


def login_to_account(browser):
    creator = JsonCommandCreator(browser, 'files/travian/login.json')
    command = creator.create_command()
    command.execute()


def open_resources(browser):
    creator = JsonCommandCreator(browser, 'files/travian/open_resources.json')
    command = creator.create_command()
    command.execute()


def getVillage(browser):
    css = '#sidebarBoxVillagelist > .sidebarBoxInnerBox > div > ul > .active > a > div.name'
    elem = browser.find_element_by_css_selector(css)
    return Village(browser, elem.text)
