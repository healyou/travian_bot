from utils.util import *
from utils.context import Context
from village.villages import *
import time


browser = open_travian()
Context.browser = browser
try:
    login_to_account(browser)
    village = getVillage(browser)
    village.run()

except OSError as err:
    print('Ошибка работы скрипта')
finally:
    time.sleep(5)
    browser.quit()
    print('Завершение работы скрипта')

# TODO делать далее
# 2)Исправить выбор типа поля для стрительства (не то выбирает почему-то)
# 3)Сделать классы с ошибками + посетитель