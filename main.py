from selenium.webdriver import Chrome
from command.creator.factory import *
from command.commands import FactoryCommand
from utils.util import *
from village.villages import *


browser = open_travian()
try:
    login_to_account(browser)
    village = getVillage(browser)
    village.analyze()
    type = village.get_next_build_field_type()
    print ('Тип здания для постройки ' + type)

    # Текущее строительство и время до его завершения
    fields = browser.find_elements_by_css_selector('div[class=\'buildDuration\'] > span')
    if (len(fields) > 0):
        for field in fields:
            print ('Здание ещё строится сек. - ' + field.get_attribute('value'))
    else:
        name_for_search = {
            Production.WOOD.value: '',
            Production.IRON.value: 'Железный рудник Уровень',
            Production.CLAY.value: '',
        }[type]

        # Информация обо всех полях деревни
        fields = browser.find_elements_by_css_selector('area[shape=\'circle\']')
        for field in fields:
            name = field.get_attribute('alt')
            if (name_for_search in name):
                # надо определять поле с наименьшим уровнем для строительства
                # и пытаться строить его
                print (name)

        # Строим 9 здание
        # field = browser.find_element_by_css_selector('area[href=\'build.php?id=9\']')
        # field.click()
        # field = browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button')
        # field.click()
        pass

except OSError as err:
    print('Ошибка')
finally:
    browser.quit()
    print('Завершение работы')
