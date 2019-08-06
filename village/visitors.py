from abc import ABCMeta, abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from utils.context import Context
# TODO - почему python не может import циклический разрулить?


class BuildFieldExceptionVisitor(object):
    def visit(self, exception: BuildFieldException) -> None:
        self.exception = exception
        print('Ошибка строительства здания: ' + str(exception))

        exc_method = {
            BuildFieldExceptionType.NOT_ENOUGH_FOOD: self.onNotEnoughFood,
            BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE: self.onBuildButtonUnavailable
        }.get(exception.type, self.onIllegalException)
        exc_method()
    
    def onNotEnoughFood(self):
        if (Context.buildCornOnError):
            print('Попытка построить ферму')
            # self.tryToBuildField(Production.CORN.value)

    def onBuildButtonUnavailable(self):
        pass

    def onIllegalException(self):
        print('Неизвестная ошибка строительства здания')