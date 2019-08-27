import time

from command.queue.buildthread import BuildThread
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import login_to_account, open_travian

browser = open_travian()
try:
    login_to_account(browser)
    
    Context.browser = browser
    Context.queueProperties = QueueProperties(browser)

    thread = BuildThread(Context.queueProperties)
    thread.start()

    thread.stop()
    thread.join()

except OSError as err:
    print('Ошибка работы скрипта')
finally:
    time.sleep(5)
    print('Завершение работы скрипта')
    browser.quit()

# делать далее
# TODO 2)Сделать очередь обработки command, которые создают здания (можно добавлять туда задачи и всё) увязать с деревнями
# TODO 3)Сделать отдельный поток на строительство зданий
# TODO 4)Определение, когда необходимо строить склад и амбар и их постройка
# TODO 5)Строительство полей и складов с амбарами вместе
# TODO 6)Рефакторинг провести в коде
