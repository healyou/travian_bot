from .abstractquerybuilder import Operation, AbstractExpression, MatchMode
from abc import abstractmethod
from typing import List


class SimpleExpression(AbstractExpression):
    # Символ подстановки по умолчанию
    DEFAULT_PLACEHOLDER: str = '?'

    def __init__(self, fieldName: str, arg: object, operation: Operation):
        self.__fieldName: str = fieldName
        self.__arg: object = arg
        self.__operation: Operation = operation

    @abstractmethod
    def hasValue(self) -> bool:
        return self.__arg is not None

    @abstractmethod
    def getSqlString(self) -> str:
        return self.__fieldName + ' ' + self.__operation.value + " " + self.DEFAULT_PLACEHOLDER 

    @abstractmethod
    def getArguments(self) -> List[object]:
        return [self.__arg]


# Поместить выражение в скобки
class Parentheses(AbstractExpression):
    def __init__(self, expression: AbstractExpression):
        if (expression is None):
            raise Exception('Expression expected for parentheses')
        self.__expressiong: AbstractExpression = expression

    @abstractmethod
    def hasValue(self) -> bool:
        return self.__expressiong.hasValue()

    @abstractmethod
    def getSqlString(self) -> str:
        return '(' + self.__expressiong.getSqlString() + ')'

    @abstractmethod
    def getArguments(self) -> List[object]:
        return self.__expressiong.getArguments()
        

# TODO ne (Добавить условие поиска по текстовому полю на неравенство) - надо додобавить методы для даты и другого)
# TODO ge (Добавить условие поиска >= по текстовому полю)
# TODO le (Добавить условие поиска <= по текстовому полю)
# TODO gt (Добавить условие поиска > по текстовому полю)
# TODO lt (Добавить условие поиска < по текстовому полю)
# TODO like (Добавить условие поиска like)
# TODO ilike (Добавить условие поиска like без учета регистра символов)
# TODO between (Добавить условие поиска в диапазоне значений по числовому полю. Границы диапазона могут быть пустыми)
# TODO isNull (Добавить условие на пустое поле)
# TODO isNotNull (Добавить условие на непустое поле)
# TODO in (Добавить условие поиска по текстоваому полю в списке значений)
# TODO not (Добавить отрицпне условия)