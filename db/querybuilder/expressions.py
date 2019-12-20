from .abstractquerybuilder import Operation, AbstractExpression
from abc import abstractmethod
from typing import List


class EqExpression(AbstractExpression):
    # Символ подстановки по умолчанию
    DEFAULT_PLACEHOLDER: str = '?'

    def __init__(self, fieldName: str, arg: object):
        self.__fieldName: str = fieldName
        self.__arg: object = arg
        self.__operation: Operation = Operation.EQ

    @abstractmethod
    def hasValue(self) -> bool:
        return self.__arg is not None

    @abstractmethod
    def getSqlString(self) -> str:
        return self.__fieldName + ' ' + self.__operation.value + " " + self.DEFAULT_PLACEHOLDER 

    @abstractmethod
    def getArguments(self) -> List[object]:
        return [self.__arg]