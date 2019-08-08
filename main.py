from utils.util import open_travian, open_village, getVillage, login_to_account
from utils.context import Context
from village.villages import Village
import time


browser = open_travian()
Context.browser = browser
try:
    login_to_account(browser)
    village: Village = getVillage(browser)
    open_village(browser)
    village.buildStock()

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
