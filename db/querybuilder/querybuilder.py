from __future__ import annotations
from .abstractquerybuilder import AbstractExpression, AbstractQueryBuilder
from .expressions import EqExpression
from abc import abstractmethod
from typing import List


class QueryBuilder(object):
    def __init__(self, query: str):
        self.__query: str = query
        self.__expression: AbstractExpression = None

    @abstractmethod
    def getQuery(self) -> str:
        if (self.__hasExpression()):
            return self.__query + ' ' + self.__expression.getSqlString()
        else:
            return self.__query

    @abstractmethod
    def getArguments(self) -> List[object]:
        arguments = []
        if (self.__hasExpression()):
            arguments.extend(self.__expression.getArguments())
        return arguments

    def __hasExpression(self) -> bool:
        return self.__expression is not None and self.__expression.hasValue 

    @abstractmethod
    def addPaging(self, startIndex: int, count: int) -> QueryBuilder:
        pass

    @abstractmethod
    def addSorting(self, sortOrder: SortOrder) -> QueryBuilder:
        pass

    def eq(self, fieldName: str, arg: object) -> QueryBuilder:
        return self.__addExpressionIfHasValue(EqExpression(fieldName, arg))

    def __addExpressionIfHasValue(self, expression: AbstractExpression) -> QueryBuilder:
        # TODO - множество выражений
        if (expression.hasValue()):
            self.__expression = expression
        return self

    # Добавить условие поиска
    @abstractmethod
    def addExpression(self, expression: AbstractExpression) -> QueryBuilder:
        pass