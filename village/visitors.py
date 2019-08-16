from abc import ABCMeta, abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from utils.context import Context
from village.types import Production, ProductionTypeVisitor
from village.types import IndoorBuildingType, IndoorBuildingTypeVisitor


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


# Посетитель, который в зависимости от типа ресурсного поля вернёт строку
# по которой надо искать элемент в web интерфейсе
class ProductionFieldSearchNameVisitor(ProductionTypeVisitor):
    def visitWood(self):
        return 'Лесопилка Уровень'

    def visitClay(self):
        return 'Глиняный карьер Уровень'

    def visitIron(self):
        return 'Железный рудник Уровень'

    def visitCorn(self):
        return 'Ферма Уровень'


class IndoorBuildingTypeSearchNameVisitor(IndoorBuildingTypeVisitor):
    @abstractmethod
    def visitStock(self):
        return 'Склад'

    @abstractmethod
    def visitGranary(self):
        return 'Амбар'

    @abstractmethod
    def visitResidence(self):
        return 'Резиденция'

    @abstractmethod
    def visitHedge(self):
        return 'Изгородь'

    @abstractmethod
    def visitWorkshop(self):
        return 'Мастерская'