from enum import Enum


class BuildFieldExceptionType(Enum):
    NOT_ENOUGH_FOOD = 'not_enough_food'
    BUILD_BUTTON_UNAVAILABLE = 'build_button_unavailable'


# TODO посетитель на обработку различных ошибок строительства
class BuildFieldException(Exception):
    def __init__(self, message, type, village):
        super(BuildFieldException, self).__init__(message)
        self.type = type
        self.village = village

    def accept(self, visitor) -> None:
        visitor.visit(self)