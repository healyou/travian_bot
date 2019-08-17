from enum import Enum


class BuildFieldExceptionType(Enum):
    NOT_ENOUGH_FOOD = 'not_enough_food'
    BUILD_BUTTON_UNAVAILABLE = 'build_button_unavailable'
    NOT_ENOUGH_PLACE = 'not_enough_place'
    INSUFFICIENT_GRANARY_CAPACITY = 'insufficient_granary_capacity'
    INSUFFICIENT_STOCK_CAPACITY = 'insufficient_stock_capacity'
    INSUFFICIENT_ALL_CAPACITY = 'insufficient_capacity'
    UNKNOWN_ERROR = 'unknown_error'
    NOT_ENOUGH_RESOURCES = 'not_enough_resources'


class BuildFieldException(Exception):
    def __init__(self, message, type):
        super(BuildFieldException, self).__init__(message)
        self.type = type

    def accept(self, visitor) -> None:
        visitor.visit(self)