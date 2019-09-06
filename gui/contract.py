from abc import abstractmethod


class IView(object):
    # Отобразить страницу авторизации
    @abstractmethod
    def showLoginWindow(self):
        pass

    # Отобразить страницу ввода параметров работы бота
    # Начальные настройки параметров работы бота
    @abstractmethod
    def showVillagePropertiesWindow(self, default_properties):
        pass

    # Отобразить страницу работы бота
    @abstractmethod
    def showBotWorkingWindow(self):
        pass

    # Блокировка интерфеса
    @abstractmethod
    def disableWindow(self):
        pass

    # Возобновление доступности интерфейса
    @abstractmethod
    def enableWindow(self):
        pass

    # Выход из приложения
    @abstractmethod
    def quit(self):
        pass


class IPresenter(object):
    @abstractmethod
    def login(self, server_url: str, login: str, psw: str):
        pass
    
    # Начало работы бота
    # properties - параметры работы бота для каждой из деревень
    @abstractmethod
    def startWork(self, properties):
        pass

    # Завершение работы бота
    @abstractmethod
    def stopWork(self):
        pass

    # Завершение работы
    @abstractmethod
    def quit(self):
        pass
