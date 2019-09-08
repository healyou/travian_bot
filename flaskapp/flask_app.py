from flask import Flask
from threading import Thread
from flask import request
import time
from command.queue.dataclasses import *
import json


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
        super(BotController, self).__init__(__name__)


class FlaskApp(Flask):
    def __init__(self): 
        super(FlaskApp, self).__init__(__name__)
        
        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self.add_url_rule('/villages_info', view_func=self.villagesInfo)
        self.add_url_rule('/startWork', view_func=self.startWork, methods=['POST'])

    def index(self):
        return 'Hello World!'

    def login(self):
        error = ''
        try:
            if request.method == "POST":
                data = request.get_json()
                # server_url = str(args.get('server_url'))
                # login = str(args.get('login'))
                # password = str(args.get('password'))

                print (data)

                return 'True'

            return 'False'
        except Exception as e:
            print (str(e))
            return 'False'

    def startWork(self):
        try:
            if request.method == "POST":
                data = request.get_json()
                if isinstance(data, dict):
                    print ('dict')

                infos = []
                for build_vil_info in data['info_list']:
                    info_data = build_vil_info['info']
                    point = Point(info_data['point']['x'], info_data['point']['y'])
                    info = VillageInfo(info_data['name'], point)
                    auto_build_res = bool(build_vil_info['auto_build_res'])
                    infos.append(BuildVillageInfo(info, auto_build_res))
                
                properties = BuildProperties(infos)
                print(properties)

                return 'True'

            return 'False'
        except Exception as e:
            print (str(e))
            return 'False'

    def villagesInfo(self):
        infos = []
        for i in range(3):
            info = VillageInfo(str(i), Point(i,i))
            infos.append(BuildVillageInfo(info, False))
        prop = BuildProperties(infos)
        return json.dumps(prop, cls=BuildPropertiesEncoder)


class FlaskThread(Thread):
    def __init__(self): 
        super(FlaskThread, self).__init__()
        self.daemon = True

    def run(self):
        self.__app: Flask = FlaskApp()
        self.__app.run(debug=True, use_reloader=False)
