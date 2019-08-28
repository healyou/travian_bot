import threading
import time, datetime
from command.queue.properties import QueueProperties
from command.commands import AbstractCommand


# Поток, запускающий выполнение функции через каждый n секунд после очередного запуска
class BuildThread(threading.Thread):
    RERUN_SECONDS = 5

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
        print ('Запуск цикла постройки полей в потоке')
        threading.Thread(target=self.build, daemon=True).run()
        while not self.isStopped():
            # Через n секунду начнёт выполнять снова
            print ('Запуск цикла постройки полей в потоке')
            threading.Timer(self.RERUN_SECONDS, self.build).run()
        print ('Конец выполнения работы потока')
    
    def build(self):
        self.__properties.analizeAutoBuildForAllVillages()
        command: AbstractCommand = self.__properties.getNextBuildingCommand()

        # для теста - если во второй раз не нашли команды для выполнения - выход
        if (command is None):
            print ('Не найдены команды для выполнения')
            self.stop()
            return

        while command is not None:
            print ('Выполнение команды в потоке')
            command.execute()
            command = self.__properties.getNextBuildingCommand()
        print ('Все команды в текущем цикле постройки выполнены')

# TODO - добавить сюда следующее
# TODO 1)Выполнение строительства полей
# TODO 2)Анализ переполнения складов и амбаров
# TODO 3)Анализ времени для запуска следующего строительства здания