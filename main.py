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

# делать далее
# TODO 1)Исправить выбор типа поля для стрительства (не то выбирает почему-то)
# TODO 2)Рефакторинг провести в коде
# TODO 3)Делать задачи - чтобы здания строились автоматически