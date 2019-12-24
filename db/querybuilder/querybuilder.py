from __future__ import annotations

from abc import abstractmethod
from typing import List

from .abstractquerybuilder import (AbstractExpression, AbstractQueryBuilder,
                                   MatchMode, Operation)
from .expressions import Parentheses, SimpleExpression, LogicalExpression


class QueryBuilder(object):
    # т.к. нельзя добавить 2 конструктора, то вводим для args значение по умолчанию
    def __init__(self, query: str, args: List[object] = []):
        self.__query: str = query
        self.__args: List[object] = args
        self.__expression: AbstractExpression = None
        self.__sortBy: str = None
        self.__paging: str = None
        self.__pagingStartIndex: int = None
        self.__pagingCount: int = None

    @abstractmethod
    def getQuery(self) -> str:
        sqlQuery = ''

        # Основное выражение
        if (self.__hasExpression()):
            sqlQuery += self.__query + ' where ' + self.__expression.getSqlString()
        else:
            sqlQuery += self.__query

        # Сортировка
        if (self.__sortBy):
            sqlQuery += self.__sortBy

        # Пагинация
        if (self.__paging):
            sqlQuery += self.__paging

        return sqlQuery

    @abstractmethod
    def getArguments(self) -> List[object]:
        arguments = []

        # Начальные параметры
        if (self.__args):
            arguments.extend(self.__args)
        
        # Основное выражение
        if (self.__hasExpression()):
            arguments.extend(self.__expression.getArguments())
        
        # Пагинация
        if (self.__paging):
            arguments.append(self.__pagingStartIndex)
            arguments.append(self.__pagingCount - 1)
        
        return arguments

    def __hasExpression(self) -> bool:
        return self.__expression is not None and self.__expression.hasValue 

    @abstractmethod
    def addPaging(self, startIndex: int, count: int) -> QueryBuilder:
        self.__pagingStartIndex = startIndex
        self.__pagingCount = count
        self.__paging = ' limit ?, ?'
        return self

    @abstractmethod
    def addSorting(self, fieldName: str, sortOrder: SortOrder) -> QueryBuilder:
        # Поле не пустое
        if (not fieldName):
            raise Exception('Expected fieldName')

        self.__initAndAddSortByCommaIfNeeded()
        self.__sortBy += f'{fieldName} {sortOrder.value}'

    def __initAndAddSortByCommaIfNeeded(self):
        if (self.__sortBy):
            self.__sortBy += ', '
        else:
            self.__sortBy = ' order by '

    def eq(self, fieldName: str, arg: object) -> QueryBuilder:
        return self.__addExpressionIfHasValue(SimpleExpression(fieldName, arg, Operation.EQ))

    def parentheses(self, expression: AbstractExpression) -> QueryBuilder:
        return self.__addExpressionIfHasValue(Parentheses(expression))

    def neForString(self, fieldName: str, arg: str):
        argument = MatchMode.EXACT.toMatchString(arg)
        return self.__addExpressionIfHasValue(SimpleExpression(fieldName, argument, Operation.NE))
    def neForValue(self, fieldName: str, arg: object) -> QueryBuilder:
        # Для строки один случай %str%
        # Для даты другой случай ? != trunc(date)
        # Для остальных значений можно юзать простой exp  ? != value
        return self.__addExpressionIfHasValue(SimpleExpression(fieldName, arg, Operation.NE))

    def like(self, fieldName: str, arg: str, matchMode: MatchMode) -> QueryBuilder:
        argument = matchMode.toMatchString(arg)
        return self.__addExpressionIfHasValue(SimpleExpression(fieldName, argument, Operation.LIKE))

    def iLike(self, fieldName: str, arg: str, matchMode: MatchMode) -> QueryBuilder:
        argument = matchMode.toMatchString(arg)
        upperFieldName = f'upper({fieldName})'
        return self.__addExpressionIfHasValue(SimpleExpression(upperFieldName, argument, Operation.LIKE))

    def between(self, fieldName: str, fromValue: object, toValue: object) -> QueryBuilder:
        ge = SimpleExpression(fieldName, fromValue, Operation.GE)
        le = SimpleExpression(fieldName, toValue, Operation.LE)
        andExp = LogicalExpression(Operation.AND, [ge, le])
        return self.__addExpressionIfHasValue(andExp)

    def __addExpressionIfHasValue(self, expression: AbstractExpression) -> QueryBuilder:
        # TODO - множество выражений
        if (expression.hasValue()):
            self.__expression = expression
        return self

    # Добавить условие поиска
    @abstractmethod
    def addExpression(self, expression: AbstractExpression) -> QueryBuilder:
        pass
