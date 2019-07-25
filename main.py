from selenium.webdriver import Chrome
from command.creator.factory import *
from command.commands import FactoryCommand
from utils.util import get_absolute_file_path

browser = Chrome(executable_path='install/chromedriver.exe')
try:
    browser.get('https://ts3.travian.ru')
    file_path = get_absolute_file_path(__file__, 'files/open_travian.json')
    creator = JsonCommandCreator(browser, file_path)
    command = creator.create_command()
    command.execute()
except OSError as err:
    print('Ошибка')
finally:
    browser.quit()
    print('Завершение работы')