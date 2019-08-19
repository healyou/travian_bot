import threading
import time, datetime


# Поток, запускающий выполнение функции через каждый n секунд после очередного запуска
class BuildThread(threading.Thread):
    RERUN_SECONDS = 1

    def __init__(self):
        super(BuildThread, self).__init__()
        self.daemon = True

    def run(self):
        while True:
            print('startRunThread=' + str(time.ctime()))
            # Через 1 секунду начнёт выполнять снова
            threading.Timer(self.RERUN_SECONDS, self.build).run()
            print('endRunThread=' + str(time.ctime()))
    
    def build(self):
        print('start=' + str(time.ctime()))
        # Выполнение работы потока
        print('thread work')
        time.sleep(2)
        print('end=' + str(time.ctime()))

# TODO - добавить сюда следующее
# TODO 1)Выполнение строительства полей
# TODO 2)Анализ переполнения складов и амбаров
# TODO 3)Анализ времени для запуска следующего строительства здания