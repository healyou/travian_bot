import threading
import time, datetime
from command.queue.properties import QueueProperties
from command.commands import AbstractCommand


# Поток, запускающий выполнение функции через каждый n секунд после очередного запуска
class BuildThread(threading.Thread):
    RERUN_SECONDS = 1

    def __init__(self, properties: QueueProperties):
        super(BuildThread, self).__init__()
        self.daemon: bool = True
        self.__properties: QueueProperties = properties

    def run(self):
        threading.Thread(self.build).run()
        # while True:
        # Через 1 секунду начнёт выполнять снова
        # threading.Timer(self.RERUN_SECONDS, self.build).run()
    
    def build(self):
        print('start=' + str(time.ctime()))

        self.__properties.analizeBuildings()
        command = self.__properties.getNextBuildingCommand()
        if (command is not None):
            print ('Выполнение команды в потоке')
            command.execute()
        else:
            print ('Не найдена команда для выполнения в потоке')

        print('end=' + str(time.ctime()))

# TODO - добавить сюда следующее
# TODO 1)Выполнение строительства полей
# TODO 2)Анализ переполнения складов и амбаров
# TODO 3)Анализ времени для запуска следующего строительства здания