from gui.contract import IView

import time
from tkinter import *

from command.queue.buildthread import BuildThread
from command.queue.properties import QueueProperties
from utils.context import Context
from utils.travian_utils import login_to_account, open_travian


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
        self.root = Tk()
        self.root.title("GUI на Python")
        self.root.geometry("640x480")

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

    def authorization(self):
        self.main_frame.disable()

        browser = open_travian()
        try:
            login_to_account(browser)
            
            Context.browser = browser
            Context.queueProperties = QueueProperties(browser)

        except OSError as err:
            print('Ошибка работы скрипта')
        finally:
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            time.sleep(5)
            print('Завершение работы скрипта')
            browser.quit()
        
        self.main_frame.enable()
        self.setupVillageInfoFrame()

    def setupVillageInfoFrame(self):
        server_frame = Frame(self.main_frame)
        server_label = Label(master=server_frame, text='Настройка автоматического строительства')
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
        self.main_frame.pack(fill=BOTH, expand=YES)
        