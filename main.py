import time

from command.queue.buildthread import BuildThread
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import login_to_account, create_browser

browser = create_browser()
try:
    login_to_account(browser)
    
    Context.browser = browser
    Context.queueProperties = QueueProperties(browser)

    thread = BuildThread(Context.queueProperties)
    thread.start()
    thread.join()

except OSError as err:
    print('Ошибка работы скрипта')
finally:
    time.sleep(5)
    print('Завершение работы скрипта')
    browser.quit()
