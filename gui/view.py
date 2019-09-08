from gui.contract import IView, IPresenter
from gui.presenter import Presenter

import time
from tkinter import *

from command.queue.buildthread import BuildThread
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import login_to_account, open_travian, create_browser
from utils.util import getVillagesInfo
from gui.scrolled_view import VerticalScrolledFrame
from gui.disable_frame import dFrame
from command.queue.dataclasses import *


class View(IView):
    def __init__(self): 
        super(View, self).__init__()
        self.root: Tk = Tk()
        self.root.title("GUI на Python")
        self.root.geometry("640x480")
        self.root.protocol("WM_DELETE_WINDOW", self.onQuit)
        self.root.bind("<Destroy>", self.onDestroy)
        self.main_frame = dFrame(self.root)

        self.__presenter: IPresenter = Presenter(self)

        self.__build_properties: BuildProperties = None
        self.__auto_build_vars: list = None
    
    def mainloop(self):
        self.showLoginWindow()
        self.root.mainloop()

    def onQuit(self):
        self.__presenter.quit()

    def onDestroy(self, event):
        pass
        # Вызывается каждый раз, когда удаляется компонент в иерархии(все дочерние)
        # print ('onDestroy')

    def authorization(self):
        self.__presenter.login('', '', '')

    def startBotWork(self):
        for index, item in enumerate(self.__auto_build_vars):
            self.__build_properties.info_list[index].auto_build_res = bool(item.get())

        self.__presenter.startWork(self.__build_properties)

    def stopBotWork(self):
        self.__presenter.stopWork()

    def showLoginWindow(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        server_frame = Frame(self.main_frame)
        server_label = Label(master=server_frame, text='Сервер')
        server_label.pack(side="left")
        server_choices = [
            'https://ts3.travian.ru',
            'test_server_1',
            'test_server_2'
        ]
        server = StringVar()
        server.set(server_choices[0])
        server_choice = OptionMenu(server_frame, server, *server_choices)
        server_choice.pack(side="left", fill='x')
        server_frame.pack(fill='x')


        login_frame = Frame(self.main_frame)
        login_label = Label(master=login_frame, text='Логин')
        login_label.pack(side="left")
        login = StringVar()
        login_entry = Entry(master=login_frame, textvariable=login)
        login_entry.pack(side="left", fill='x')
        login_frame.pack(fill='x')


        psw_frame = Frame(self.main_frame)
        psw_label = Label(master=psw_frame, text='Пароль')
        psw_label.pack(side="left")
        psw = StringVar()
        psw_entry = Entry(master=psw_frame, show='*', textvariable=psw)
        psw_entry.pack(side="left", fill="x")
        psw_frame.pack(fill='x')


        message_button = Button(master=self.main_frame, text='Авторизация', command=self.authorization)
        message_button.pack(side="top", fill="x")

        self.main_frame.pack(fill=BOTH, expand=YES)

    def showVillagePropertiesWindow(self, default_properties: BuildProperties):
        self.__build_properties = default_properties

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        width = 640
        height = 480
        villages_properties_frame = VerticalScrolledFrame(
            self.main_frame,
            width=width,
            height=height
        )

        info_frame = Frame(villages_properties_frame)
        info_label = Label(master=info_frame, text='Настройка параметров работы бота')
        info_label.pack()
        start_button = Button(master=info_frame, text='Начать работу бота', command=self.startBotWork)
        start_button.pack(fill='x')
        info_frame.pack(side='top', fill='x')

        props_frame = Frame(villages_properties_frame)
        self.__auto_build_vars = []
        for info in default_properties.info_list:
            build_info: BuildVillageInfo = info
            vil_prop_frame = Frame(props_frame)

            info_label = build_info.info.name + ' :(' + str(build_info.info.point.x) + '|' + str(build_info.info.point.y) + ')'
            vil_info_label = Label(master=vil_prop_frame, text=info_label)
            vil_info_label.pack(side='left')

            auto_build_var = IntVar()
            auto_build_var.set(int(build_info.auto_build_res))
            button = Checkbutton(
                vil_prop_frame, 
                text='Автоматическое стр-во ресурсов в деревне', 
                variable=auto_build_var
            )
            self.__auto_build_vars.append(auto_build_var)
            button.pack(side='left', fill='x')

            vil_prop_frame.pack(side='top', fill='x')
        props_frame.pack(side='top', fill=BOTH)
        
        villages_properties_frame.pack(fill=BOTH, expand=YES)
        self.main_frame.pack(fill=BOTH, expand=YES)

    def showBotWorkingWindow(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        server_frame = Frame(self.main_frame)
        server_label = Label(master=server_frame, text='Лог работа бота')
        server_label.pack(side="left")

        message_button = Button(master=self.main_frame, text='Завершить работу', command=self.stopBotWork)
        message_button.pack(side="top", fill="x")

        self.main_frame.pack(fill=BOTH, expand=YES)

    def disableWindow(self):
        self.main_frame.disable()

    def enableWindow(self):
        self.main_frame.enable()

    def quit(self):
        self.root.destroy()
