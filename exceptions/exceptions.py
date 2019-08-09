from enum import Enum


class BuildFieldExceptionType(Enum):
    NOT_ENOUGH_FOOD = 'not_enough_food'
    BUILD_BUTTON_UNAVAILABLE = 'build_button_unavailable'
    NOT_ENOUGH_PLACE = 'not_enough_place'


class BuildFieldException(Exception):
    def __init__(self, message, type):
        super(BuildFieldException, self).__init__(message)
        self.type = type

    def accept(self, visitor) -> None:
        visitor.visit(self)