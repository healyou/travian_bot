import threading
import time, datetime
from command.queue.properties import QueueProperties
from command.commands import AbstractCommand


# Поток, запускающий выполнение функции через каждый n секунд после очередного запуска
class BuildThread(threading.Thread):
    RERUN_SECONDS = 360

    def __init__(self, properties: QueueProperties):
        super(BuildThread, self).__init__()
        self.daemon: bool = True
        self.__stop = threading.Event() 
        self.__properties: QueueProperties = properties

    def stop(self):
        print ('Стопим поток')
        self.__stop.set()
  
    # see isAlive для проверки выполнения работы потока
    def isStopped(self): 
        return self.__stop.isSet()

    def run(self):
        # Первый раз запускаем сразу
        threading.Thread(target=self.build, daemon=True).run()
        while not self.isStopped():
            # Через n секунду начнёт выполнять снова
            threading.Timer(self.RERUN_SECONDS, self.build).run()
        print ('Конец выполнения работы потока')
    
    def build(self):
        self.__properties.analizeBuildings()
        command = self.__properties.getNextBuildingCommand()
        if (command is not None):
            print ('Выполнение команды в потоке')
            command.execute()
        else:
            print ('Не найдена команда для выполнения в потоке')

# TODO - добавить сюда следующее
# TODO 1)Выполнение строительства полей
# TODO 2)Анализ переполнения складов и амбаров
# TODO 3)Анализ времени для запуска следующего строительства здания