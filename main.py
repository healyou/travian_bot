from utils.util import *
from utils.context import Context
from village.villages import *
import time


browser = open_travian()
Context.browser = browser
try:
    login_to_account(browser)
    village: Village = getVillage(browser)
    open_village(browser)

    # надо найти все элементы, потом делать по ним hover и определять, что построено на данном месте
    elems = browser.find_elements_by_css_selector('div#village_map > div.buildingSlot')
    k = 1
    from selenium.webdriver.common.action_chains import ActionChains
    for elem in elems:
        element_to_hover_over = elem
        hover = ActionChains(browser).move_to_element(element_to_hover_over)
        hover.perform()
        # здесь текст основных зданий
        hover_elem_tytle = browser.find_element_by_css_selector('div.tip > div.tip-container > div.tip-contents > div.title.elementTitle')
        # здесь будет текст стройплощадки-пустое место для строительства
        hover_elem_text = browser.find_element_by_css_selector('div.tip > div.tip-container > div.tip-contents > div.text.elementText')
        # print ('title=' + hover_elem_tytle.text + ' text=' + hover_elem_text.text)

        if ('123Стройплощадка' in hover_elem_text.text):
            # по остальным нельзя клинуть - св-во pointer-events: None - только для стройплощадки
            click_item = element_to_hover_over.find_element_by_css_selector('.hoverShapeWinter')
            click_item.click()
            break

        # Получаем текст первого уровня
        all_text = hover_elem_tytle.text
        child_elems = hover_elem_tytle.find_elements_by_xpath("./*")
        parent_text = all_text
        for child in child_elems:
            parent_text = parent_text.replace(child.text, '')
        print ('one_level_text=' + parent_text)
        if ('Главное здание' in parent_text):
            # у построенных зданий можно кликать по самому элементу или по уровню
            click_item = element_to_hover_over.find_element_by_css_selector('.level')
            click_item.click()
            # element_to_hover_over.click()
            break

        # first_lvl_title = hover_elem_tytle.find_elements_by_xpath("./*")
        # for ggwp in first_lvl_title:
        #     print ('flvltitle=' + ggwp.text)
    

    # village.run()

except OSError as err:
    print('Ошибка работы скрипта')
finally:
    time.sleep(5)
    print('Завершение работы скрипта')
    browser.quit()

# делать далее
# TODO 1)Постройка амбара и склада с нуля и на готовом
# TODO 2)Определение, когда необходимо строить склад и амбар и их постройка
# TODO 3)Цикл строительства полей
# TODO 4)Строительство полей и складов с амбарами вместе
# TODO 5)Очередь строительства зданий - или автоматическое строительство
# TODO 6)Рефакторинг провести в коде
