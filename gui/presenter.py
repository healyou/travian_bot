import time
from gui.contract import IPresenter, IView
from command.queue.buildthread import BuildThread
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import login_to_account, open_travian, create_browser
from utils.util import getVillagesInfo


# TODO - надо переписать на rest сервис, т.к. потом этот класс
# должен будет общаться с рест сервисом
class Presenter(IPresenter):
    def __init__(self, view: IView): 
        super(Presenter, self).__init__()
        self.__login: bool = False
        self.__view: IView = view
        self.__build_thread: BuildThread = None

    def login(self, server_url: str, login: str, psw: str):
        self.__view.disableWindow()

        try:
            browser = create_browser()
            Context.browser = browser

            open_travian(browser)
            login_to_account(browser)
            
            Context.queueProperties = QueueProperties(browser)

            self.__view.enableWindow()
            # TODO - передача дефолтных параметров
            self.__view.showVillagePropertiesWindow([])

        except Exception as err:
            print (str(err))
            print('Ошибка работы скрипта')
            time.sleep(5)
            print('Завершение работы скрипта')
            if (Context.browser is not None):
                Context.browser.quit()
            Context.browser = None
            Context.queueProperties = None
            Context.buildCornOnError = True

            self.__view.enableWindow()
    
    def startWork(self, properties):
        print ('Начало работы бота')
        if (self.__build_thread is not None):
            raise Exception('Поток строительства уже запущен')
        else:
            self.__build_thread = BuildThread(Context.queueProperties)
            self.__build_thread.start()

            self.__view.showBotWorkingWindow()

    def stopWork(self):
        if (self.__build_thread is not None):
            self.__build_thread.stop()
            self.__build_thread.join()
            self.__build_thread = None

        if (Context.browser is not None):
            Context.browser.quit()

            Context.browser = None
            Context.queueProperties = None
            Context.buildCornOnError = True

        self.__view.showLoginWindow()

    def quit(self):
        self.stopWork()
        self.__view.quit()

    def __isLogin(self) -> bool:
        return self.__login