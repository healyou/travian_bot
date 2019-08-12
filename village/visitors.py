from abc import ABCMeta, abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from utils.context import Context


class BuildFieldExceptionVisitor(object):
    def visit(self, exception: BuildFieldException) -> None:
        self.exception = exception
        print('Ошибка строительства здания: ' + str(exception))

        exc_method = {
            BuildFieldExceptionType.NOT_ENOUGH_FOOD: self.onNotEnoughFood,
            BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE: self.onBuildButtonUnavailable,
            BuildFieldExceptionType.NOT_ENOUGH_PLACE: self.onNotEnoughPlace,
            BuildFieldExceptionType.INSUFFICIENT_CAPACITY: self.onInsufficientCapacity,
            BuildFieldExceptionType.NOT_ENOUGH_RESOURCES: self.onNotEnoughResources,
            BuildFieldExceptionType.UNKNOWN_ERROR: self.onUnknownError
        }.get(exception.type, self.onIllegalException)
        exc_method()
    
    def onNotEnoughFood(self):
        if (Context.buildCornOnError):
            print('Попытка построить ферму')
            # self.tryToBuildField(Production.CORN.value)

    def onBuildButtonUnavailable(self):
        pass
        # print('Кнопка строительства недоступна')

    def onNotEnoughPlace(self):
        pass
        # print('Нет места для строительства')

    def onInsufficientCapacity(self):
        pass
        # TODO - может быть склад и амбар
        # print('Недостаточна вместимость')

    def onNotEnoughResources(self):
        pass
        # print('Недостаточно ресурсов')

    def onUnknownError(self):
        pass
        # print('Не классифицируемая ошибка')

    def onIllegalException(self):
        print('Неизвестная ошибка строительства здания - IllegalException')