from gui.contract import IView

import time
from tkinter import *

from command.queue.buildthread import BuildThread
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import login_to_account, open_travian, create_browser
from utils.util import getVillagesInfo
from gui.scrolled_view import VerticalScrolledFrame


class dFrame(Frame):
    def enable(self, state='!disabled'):
        def cstate(widget):
            # Is this widget a container?
            if widget.winfo_children:
                # It's a container, so iterate through its children
                for w in widget.winfo_children():
                    # change its state
                    w.state((state,))
                    # and then recurse to process ITS children
                    cstate(w)

            cstate(self)

    def disable(self):
        self.enable('disabled')

class View(IView):
    def __init__(self): 
        super(View, self).__init__()
        self.root: Tk = Tk()
        self.root.title("GUI на Python")
        self.root.geometry("640x480")

        self.root.protocol("WM_DELETE_WINDOW", self.onQuit)
        self.root.bind("<Destroy>", self.onDestroy)

        self.main_frame = dFrame(self.root)


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
    
    def mainloop(self):
        self.root.mainloop()

    def onQuit(self):
        print ('onQuit')
        if (Context.browser is not None):
            Context.browser.quit()

            Context.browser = None
            Context.queueProperties = None
            Context.buildCornOnError = True
        self.root.destroy()

    def onDestroy(self, event):
        pass
        # Вызывается каждый раз, когда удаляется компонент в иерархии(все дочерние)
        # print ('onDestroy')

    def authorization(self):
        self.main_frame.disable()

        try:
            browser = create_browser()
            Context.browser = browser

            open_travian(browser)
            login_to_account(browser)
            
            Context.queueProperties = QueueProperties(browser)

            self.main_frame.enable()
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            self.setupVillageInfoFrame()

        except Exception as err:
            print (str(err))
            print('Ошибка работы скрипта')
            time.sleep(5)
            print('Завершение работы скрипта')
            browser.quit()

            Context.browser = None
            Context.queueProperties = None
            Context.buildCornOnError = True


    def setupVillageInfoFrame(self):
        villages_properties_frame = VerticalScrolledFrame(self.main_frame)
        villages_properties_frame.pack(fill=BOTH, expand=YES)

        info_frame = Frame(villages_properties_frame)
        info_label = Label(master=info_frame, text='Настройка параметров работы бота')
        info_label.pack(fill='x')
        start_button = Button(master=info_frame, text='Начать работу бота', command=self.startBotWork)
        start_button.pack(fill='x')
        info_frame.pack(fill='x', expand=YES)

        props_frame = Frame(villages_properties_frame)
        villages_info = getVillagesInfo(Context.browser)
        for info in villages_info:
            vil_prop_frame = Frame(props_frame)

            info_label = info.name + ' :(' + str(info.point.x) + '|' + str(info.point.y) + ')'
            vil_info_label = Label(master=info_frame, text=info_label)
            vil_info_label.pack(side='left', fill=BOTH, expand=YES)

            auto_build_var = IntVar()
            auto_build_var.set(Context.queueProperties.getVillageProps(info.point.x, info.point.y).auto_build_resources)
            Checkbutton(vil_prop_frame, text='Автоматическое стр-во ресурсов в деревне', variable=auto_build_var).pack(side='left')

            vil_prop_frame.pack(side='top', fill=BOTH, expand=YES)

        props_frame.pack(side='top', fill=BOTH, expand=YES)
        self.main_frame.pack(fill=BOTH, expand=YES)

    def startBotWork(self):
        print ('Начало работы бота')
