import time
from gui.contract import IPresenter, IView
from command.queue.buildthread import BuildThread
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import login_to_account, create_browser
from utils.util import getVillagesInfo
from command.queue.dataclasses import *
from flaskapp.flask_app import FlaskThread
import requests
import json


class DictJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__


# TODO - надо переписать на rest сервис, т.к. потом этот класс
# должен будет общаться с рест сервисом
class Presenter(IPresenter):
    def __init__(self, view: IView): 
        super(Presenter, self).__init__()
        self.__view: IView = view
        self.__flask_thread: FlaskThread = FlaskThread()
        self.__flask_thread.start()

    def login(self, server_url: str, login: str, psw: str):
        self.__view.disableWindow()

        try:
            url = 'http://127.0.0.1:5000/login'
            data = {'server_url': 'test', 'password': 'test', 'login': 'test'}               
            answer = requests.post(url, json=data)
            response_dict = answer.json()
                
            self.__view.enableWindow()

            result: bool = bool(response_dict['result'])
            if (result):
                answer = response_dict['answer']
                # load villages infos

                url = 'http://127.0.0.1:5000/villages_info'              
                answer = requests.get(url, json={})
                response_dict = answer.json()
                result: bool = bool(response_dict['result'])
                if (result):
                    answer_dict = response_dict['answer']

                    infos = []
                    for build_vil_info in answer_dict['info_list']:
                        info_data = build_vil_info['info']
                        point = Point(info_data['point']['x'], info_data['point']['y'])
                        info = VillageInfo(info_data['name'], point)
                        auto_build_res = bool(build_vil_info['auto_build_res'])
                        infos.append(BuildVillageInfo(info, auto_build_res))
                    properties = BuildProperties(infos)

                    self.__view.showVillagePropertiesWindow(properties)
                    pass
                else:
                    err: str = str(response_dict['error'])
                    raise Exception(err)
            else:
                err: str = str(response_dict['error'])
                raise Exception(err)
        except Exception as e:
            print (str(e))
            time.sleep(5)
            self.__view.enableWindow()
    
    def startWork(self, properties: BuildProperties):
        url = 'http://127.0.0.1:5000/startWork'
        json_requst = json.dumps(properties, cls=DictJsonEncoder)   
        answer = requests.post(url, data=json_requst, headers={'Content-Type': 'application/json'})
        response_dict = answer.json()
        result: bool = bool(response_dict['result'])
        if (result):
            self.__view.showBotWorkingWindow()
        else:
            print ('Ошибка начала работы бота')

    def stopWork(self):
        url = 'http://127.0.0.1:5000/stopWork'              
        answer = requests.get(url)
        response = answer.json()
        result: bool = bool(response['result'])
        if (result):
            print ('Завершение работы рест сервиса')
        else:
            err: str = str(response['error'])
            print (err)

        self.__view.showLoginWindow()

    def quit(self):
        self.stopWork()
        self.__view.quit()