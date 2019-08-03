from selenium.webdriver import Chrome
from command.creator.factory import *
from command.commands import FactoryCommand
from utils.util import *
from village.villages import *

browser = Chrome(executable_path='install/chromedriver.exe')
try:
    browser.get('https://ts3.travian.ru')

    for path in get_travian_command_files():
        file_path = get_absolute_file_path(__file__, path)
        creator = JsonCommandCreator(browser, file_path)
        command = creator.create_command()
        command.execute()

    # css = '.boxes-contents.cf > table > tbody > tr > .res'
    # elems = browser.find_elements_by_css_selector(css)

    # Информация обо всех полях деревни
    fields = browser.find_elements_by_css_selector('area[shape=\'circle\']')
    for field in fields:
        print (field.get_attribute('alt'))


    # Текущее строительство и время до его завершения
    fields = browser.find_elements_by_css_selector('div[class=\'buildDuration\'] > span')
    if (len(fields) > 0):
        for field in fields:
            print (field.get_attribute('value'))
    else:
        # Строим 9 здание
        # field = browser.find_element_by_css_selector('area[href=\'build.php?id=9\']')
        # field.click()
        # field = browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button')
        # field.click()
        pass

    village = Village(browser)
    village.analyze()
    k = 1

except OSError as err:
    print('Ошибка')
finally:
    browser.quit()
    print('Завершение работы')