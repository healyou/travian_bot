from abc import ABCMeta, abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from utils.context import Context
# TODO - почему python не может import циклический разрулить?


class BuildFieldExceptionVisitor(object):
    def visit(self, exception: BuildFieldException) -> None:
        print('Ошибка строительства здания: ' + str(exception))

        # TODO - туд должна быть обработка ошибок(посетитель)
        if (exception.type == BuildFieldExceptionType.NOT_ENOUGH_FOOD):
            if (Context.buildCornOnError):
                print('Попытка построить ферму')
                # self.tryToBuildField(Production.CORN.value)
        elif (exception.type == BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE):
            pass
        else:
            print('Неизвестная ошибка строительства здания')