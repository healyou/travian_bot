import json
import time
from threading import Thread, Event

from flask import Flask, request

from command.queue.buildthread import BuildThread
from command.queue.dataclasses import *
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import create_browser, login_to_account
from utils.util import getVillagesInfo


@dataclass
class RestAnswer(object):
    result: bool
    answer: any
    error: str


class DictJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


def configureJsonAnswer(result: bool, answer:any = None, error: str = None) -> str:
    answer = RestAnswer(result, answer, error)
    return json.dumps(answer, cls=DictJsonEncoder)


class BotController(object):
    def __init__(self): 
        super(BotController, self).__init__()
        self.__login: bool = False
        self.__started_work: bool = False
        self.__build_thread: BuildThread = None

    def login(self, server_url: str, login: str, psw: str):
        if (self.__isLogin()):
            raise Exception('Бот уже запущен')

        try:
            browser = create_browser()
            Context.browser = browser

            login_to_account(browser, server_url, login, psw)

            Context.queueProperties = QueueProperties(browser)
            self.__login = True

        except Exception as err:
            if (Context.browser is not None):
                Context.browser.quit()
            Context.browser = None
            Context.queueProperties = None
            Context.buildCornOnError = True
            raise Exception(str(err))

    def startWork(self, properties: BuildProperties):
        if (not self.__isLogin()):
            raise Exception('Необходимо авторизоваться')
        elif (self.__isStartedWork()):
            raise Exception('Бот уже запущен')

        if (self.__build_thread is not None):
            raise Exception('Поток строительства уже запущен')
        else:
            self.__build_thread = BuildThread(Context.queueProperties)
            self.__build_thread.start()
            self.__started_work = True

    def stopWork(self):
        if (not self.__isLogin()):
            raise Exception('Необходимо авторизоваться')
        else:
            self.__login = False
            if (Context.browser is not None):
                Context.browser.quit()
                Context.browser = None
                Context.queueProperties = None
                Context.buildCornOnError = True

            self.__started_work = False
            if (self.__build_thread is not None):
                self.__build_thread.stop()
                self.__build_thread.join()
                self.__build_thread = None

    def getVillagesInfo(self) -> BuildProperties:
        if (not self.__isLogin()):
            raise Exception('Бот на запущен')
        elif (self.__isStartedWork()):
            raise Exception('Нельзя получить информацию во время работы бота')

        villages_build_info = []
        for vil_info in getVillagesInfo(Context.browser):
            info: VillageInfo = vil_info
            build_info: BuildVillageInfo = BuildVillageInfo(info, False)
            villages_build_info.append(build_info)
        return BuildProperties(villages_build_info)

    def __isLogin(self) -> bool:
        return self.__login

    def __isStartedWork(self) -> bool:
        return self.__started_work

class FlaskApp(Flask):
    def __init__(self): 
        super(FlaskApp, self).__init__(__name__)

        self.__bot_controller = BotController()
        
        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self.add_url_rule('/villages_info', view_func=self.villagesInfo)
        self.add_url_rule('/startWork', view_func=self.startWork, methods=['POST'])
        self.add_url_rule('/stopWork', view_func=self.stopWork)

    def index(self):
        return configureJsonAnswer(result=True, answer='Hello World!')

    def login(self):
        try:
            if request.method == "POST":
                data = request.get_json()

                server_url = str(data['server_url'])
                login = str(data['login'])
                password = str(data['password'])

                self.__bot_controller.login(server_url, login, password)
                return configureJsonAnswer(result=True)
            else:
                return configureJsonAnswer(result=False)

        except Exception as e:
            return configureJsonAnswer(result=False, error=str(e))

    def startWork(self):
        try:
            if request.method == "POST":
                data = request.get_json()

                infos = []
                for build_vil_info in data['infoList']:
                    info_data = build_vil_info['info']
                    point = Point(info_data['point']['x'], info_data['point']['y'])
                    info = VillageInfo(info_data['name'], point)
                    auto_build_res = bool(build_vil_info['autoBuildRes'])
                    infos.append(BuildVillageInfo(info, auto_build_res))
                
                properties = BuildProperties(infos)
                self.__bot_controller.startWork(properties)
                return configureJsonAnswer(result=True)
            else:
                return configureJsonAnswer(result=False)

        except Exception as e:
            return configureJsonAnswer(result=False, error=str(e))

    def stopWork(self):
        try:
            self.__bot_controller.stopWork()
            return configureJsonAnswer(result=True)
        except Exception as e:
            return configureJsonAnswer(result=False, error=str(e))

    def villagesInfo(self):
        try:
            prop = self.__bot_controller.getVillagesInfo()
            return configureJsonAnswer(result=True, answer=prop)
        except Exception as e:
            return configureJsonAnswer(result=False, error=str(e))


class FlaskThread(Thread):
    def __init__(self): 
        super(FlaskThread, self).__init__()
        self.daemon = True

    def run(self):
        self.__app: Flask = FlaskApp()
        self.__app.run(debug=True, use_reloader=False)
