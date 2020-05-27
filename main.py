from selenium.webdriver import Chrome
from command.creator.factory import *
from command.commands import FactoryCommand
from utils.util import *

browser = Chrome(executable_path='install/chromedriver.exe')
try:
    browser.get('https://ts3.travian.ru')

    for path in get_travian_command_files():
        file_path = get_absolute_file_path(__file__, path)
        creator = JsonCommandCreator(browser, file_path)
        command = creator.create_command()
        command.execute()

except OSError as err:
    print('Ошибка')
finally:
    browser.quit()
    print('Завершение работы')