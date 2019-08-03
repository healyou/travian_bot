from selenium.webdriver import Chrome
from command.creator.factory import *
from command.commands import FactoryCommand
from utils.util import *
from utils.context import Context
from village.villages import *


def build(name_for_search):
    # Информация обо всех полях деревни
    fields = browser.find_elements_by_css_selector('div > map#rx > area[shape=\'circle\']')
    for field in fields:
        name = field.get_attribute('alt')
        if (name_for_search in name):
            # надо определять поле с наименьшим уровнем для строительства и пытаться строить его
            # возможны различные ошибки при строительстве здания - их надо централизовано все обрабатывать
            print (name)
            field.click()
            field = browser.find_element_by_css_selector('div.errorMessage > span')
            if ('Недостаток продовольствия: развивайте фермы' in field.text):
                if (Context.buildCornOnError):
                    # надо строить ферму
                    name_for_search = 'Ферма Уровень'

                    # пока скопировал строительство сюда
                    open_resources(browser)
                    fields = browser.find_elements_by_css_selector('div > map#rx > area[shape=\'circle\']')
                    for field in fields:
                        name = field.get_attribute('alt')
                        if (name_for_search in name):
                            # надо определять поле с наименьшим уровнем для строительства и пытаться строить его
                            print (name)
                            field.click()
                            field = browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button')
                            field.click()
                            break
                    # пока скопировал строительство сюда
                    
                    break
                print (field.text)
            else:
                field = browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button')
                field.click()
                break


browser = open_travian()
Context.browser = browser
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
            Production.CORN.value: 'Ферма Уровень'
        }[type]
        build(name_for_search)

except OSError as err:
    print('Ошибка')
finally:
    browser.quit()
    print('Завершение работы')
