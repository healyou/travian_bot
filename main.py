from selenium.webdriver import Chrome
from command.creator.factory import JsonFactory
from command.factorycommand import FactoryCommand
from utils.util import get_absolute_file_path

browser = Chrome(executable_path='install/chromedriver.exe')
browser.get('https://vk.com/')

file_path = get_absolute_file_path(__file__, 'files/open_friend.json')
factory = JsonFactory(browser=browser, file_path=file_path)

try:
    factory_command = FactoryCommand(factory)
    factory_command.execute()
except OSError as err:
    print('Ошибка')
finally:
    print('Завершение работы')