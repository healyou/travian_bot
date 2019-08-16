from utils.util import open_travian, open_village, getVillage, login_to_account
from utils.context import Context
from village.villages import Village
import time
from village.command.commands import *
from village.types import Production


browser = open_travian()
Context.browser = browser
try:
    login_to_account(browser)

    build = BuildProductionFieldCommand(Production.CORN, 7, 51, 91)
    # build = BuildVillageBuildingCommand(IndoorBuildingType.GRANARY, 7, 51, 91)
    build.execute()

    # OpenVillageCommand(51, 91).execute()
    # OpenVillageBuildingsCommand().execute()
    # OpenVillageResourcesCommand().execute()

    # village: Village = getVillage(browser)
    # village.run()

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
