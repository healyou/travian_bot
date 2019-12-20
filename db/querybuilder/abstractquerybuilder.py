from __future__ import annotations
from abc import abstractmethod
from enum import Enum
from typing import List

# SQL операции
class Operation(Enum):
    EQ = '='
    NE = '!='
    GE = '>='
    LE = '<='
    GT = '>'
    LT = '<'
    LIKE = 'like'
    AND = 'and'
    OR = 'or'
    IS_NULL = 'is null'
    IS_NOT_NULL = 'is not null'

# SQL сортировка
class SortOrder(Enum):
    # Сортировать в порядке возрастания.
    ASC = 'asc'
    # Сортировать в порядке убывания.
    DESC = 'desc'


# SQL выражение
class AbstractExpression(object):
    @abstractmethod
    def hasValue(self) -> bool:
        pass

    @abstractmethod
    def getSqlString(self) -> str:
        pass

    @abstractmethod
    def getArguments(self) -> List[object]:
        pass


# SQL строитель запросов
class AbstractQueryBuilder(object):
    @abstractmethod
    def getQuery(self) -> str:
        pass

    @abstractmethod
    def getArguments(self) -> List[object]:
        pass

    @abstractmethod
    def addPaging(self, startIndex: int, count: int) -> AbstractQueryBuilder:
        pass

    @abstractmethod
    def addSorting(self, sortOrder: SortOrder) -> AbstractQueryBuilder:
        pass

    # Добавить условие поиска
    @abstractmethod
    def addExpression(self, expression: AbstractExpression) -> AbstractQueryBuilder:
        pass
