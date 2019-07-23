from selenium.webdriver import Chrome
from command.creator.factory import JsonFactory
from command.factorycommand import FactoryCommand
from utils.util import get_absolute_file_path

try:
    browser = Chrome(executable_path='install/chromedriver.exe')
    browser.get('https://ts3.travian.ru')

    file_path = get_absolute_file_path(__file__, 'files/open_travian.json')
    factory = JsonFactory(browser=browser, file_path=file_path)
    factory_command = FactoryCommand(factory)
    factory_command.execute()

    # login = browser.find_element_by_css_selector('input[type=\'text\']')
    # login.click()
    # login.clear()
    # login.send_keys('healyou1994@gmail.com')

    # psw = browser.find_element_by_css_selector('input[type=\'password\']')
    # psw.click()
    # psw.clear()
    # psw.send_keys('Fjscy6SkfibDs1')

    # enter = browser.find_element_by_css_selector('button[type=\'submit\']')
    # enter.click()
except OSError as err:
    print('Ошибка')
finally:
    print('Завершение работы')

# browser.get('https://vk.com/')

# file_path = get_absolute_file_path(__file__, 'files/open_friend.json')
# factory = JsonFactory(browser=browser, file_path=file_path)

# try:
#     factory_command = FactoryCommand(factory)
#     factory_command.execute()
# except OSError as err:
#     print('Ошибка')
# finally:
#     print('Завершение работы')