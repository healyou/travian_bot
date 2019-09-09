import json
import time
from threading import Thread

from flask import Flask, request

from command.queue.buildthread import BuildThread
from command.queue.dataclasses import *
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import create_browser, login_to_account, open_travian
from utils.util import getVillagesInfo


class BuildPropertiesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BuildProperties):
            return obj.__dict__
        elif isinstance(obj, BuildVillageInfo):
            return obj.__dict__
        elif isinstance(obj, VillageInfo):
            return obj.__dict__
        elif isinstance(obj, Point):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

# class BuildPropertiesDecoder(json.JSONDecoder):
#     def __init__(self, *args, **kwargs):
#         super(BuildPropertiesDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)
    
#     def object_hook(self, dct):
#         if ('info_list' in dct):

#         if 'Actor' in dct:
#             actor = Actor(dct['Actor']['Name'], dct['Actor']['Age'], '')
#             movie = Movie(dct['Movie']['Title'], dct['Movie']['Gross'], '', dct['Movie']['Year'])
#             return Edge(actor, movie)
#         return dct


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

            open_travian(browser)
            login_to_account(browser)

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
        elif (not self.__isStartedWork()):
            raise Exception('Бот ещё не запущен')

        self.__login = False
        self.__started_work = False

        if (self.__build_thread is not None):
            self.__build_thread.stop()
            self.__build_thread.join()
            self.__build_thread = None

        if (Context.browser is not None):
            Context.browser.quit()

            Context.browser = None
            Context.queueProperties = None
            Context.buildCornOnError = True

    def getVillagesInfo(self) -> BuildProperties:
        if (not self.__isLogin()):
            raise Exception('Бот на запущен')
        elif (self.__isStartedWork()):
            raise Exception('Нельзя получить информацию во время работы бота')

        villages_build_info = []
        for vil_info in getVillagesInfo(Context.browser):
            info: VillageInfo = vil_info
            build_info: BuildVillageInfo = BuildVillageInfo(info, True)
            villages_build_info.append(build_info)
        return villages_build_info

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
        self.add_url_rule('/quit', view_func=self.quit)

    def index(self):
        return 'Hello World!'

    def login(self):
        try:
            if request.method == "POST":
                data = request.get_json()

                server_url = str(data['server_url'])
                login = str(data['login'])
                password = str(data['password'])

                self.__bot_controller.login(server_url, login, password)
                return 'True'
            else:
                return 'False'

        except Exception as e:
            return str(e)

    def startWork(self):
        try:
            if request.method == "POST":
                data = request.get_json()

                infos = []
                for build_vil_info in data['info_list']:
                    info_data = build_vil_info['info']
                    point = Point(info_data['point']['x'], info_data['point']['y'])
                    info = VillageInfo(info_data['name'], point)
                    auto_build_res = bool(build_vil_info['auto_build_res'])
                    infos.append(BuildVillageInfo(info, auto_build_res))
                
                properties = BuildProperties(infos)
                self.__bot_controller.startWork(properties)
                return 'True'
            else:
                return 'False'

        except Exception as e:
            return str(e)

    def stopWork(self):
        try:
            self.__bot_controller.stopWork()
            return 'True'
        except Exception as e:
            return str(e)

    def quit(self):
        try:
            self.__bot_controller.stopWork()
            # TODO -stop flask thread
        except Exception as e:
            return str(e)

    def villagesInfo(self):
        try:
            prop = self.__bot_controller.getVillagesInfo()
            return json.dumps(prop, cls=BuildPropertiesEncoder)
        except Exception as e:
            return str(e)


class FlaskThread(Thread):
    def __init__(self): 
        super(FlaskThread, self).__init__()
        self.daemon = True

    def run(self):
        self.__app: Flask = FlaskApp()
        self.__app.run(debug=True, use_reloader=False)
