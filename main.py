from selenium.webdriver import Chrome
from command.creator.factory import *
from command.creator.json import JsonCommandCreator
from command.commands import FactoryCommand
from utils.util import get_absolute_file_path

try:
    browser = Chrome(executable_path='install/chromedriver.exe')
    
    browser.get('https://ts3.travian.ru')
    file_path = get_absolute_file_path(__file__, 'files/open_travian.json')
    creator = JsonCommandCreator(browser, file_path)
    command = creator.create_command()
    command.execute()

    browser.get('https://vk.com/')
    file_path = get_absolute_file_path(__file__, 'files/open_friend.json')
    creator = JsonCommandCreator(browser, file_path)
    command = creator.create_command()
    command.execute()
except OSError as err:
    print('Ошибка')
finally:
    print('Завершение работы')