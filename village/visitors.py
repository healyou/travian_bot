from abc import ABCMeta, abstractmethod
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from utils.context import Context
from village.types import Production, ProductionTypeVisitor
from village.types import IndoorBuildingType, IndoorBuildingTypeVisitor, NewIndoorBuildingTypeVisitor


class BuildFieldExceptionVisitor(object):
    def visit(self, exception: BuildFieldException) -> None:
        self.exception = exception
        print('Ошибка строительства здания: ' + str(exception))

        exc_method = {
            BuildFieldExceptionType.NOT_ENOUGH_FOOD: self.onNotEnoughFood,
            BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE: self.onBuildButtonUnavailable,
            BuildFieldExceptionType.NOT_ENOUGH_PLACE: self.onNotEnoughPlace,
            BuildFieldExceptionType.INSUFFICIENT_GRANARY_CAPACITY: self.onInsufficientGranaryCapacity,
            BuildFieldExceptionType.INSUFFICIENT_STOCK_CAPACITY: self.onInsufficientStockCapacity,
            BuildFieldExceptionType.INSUFFICIENT_ALL_CAPACITY: self.onInsufficientAllCapacity,
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

    def onInsufficientGranaryCapacity(self):
        pass
        # print('Недостаточна вместимость')

    def onInsufficientStockCapacity(self):
        pass
        # print('Недостаточна вместимость')

    def onInsufficientAllCapacity(self):
        pass
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


# Поиск кнопки строительства нового здания в зависимости от типа строения
class BuildButtonNewIndoorVisitor(NewIndoorBuildingTypeVisitor):
    def __init__(self, browser, buildingName: str):
        super(BuildButtonNewIndoorVisitor, self).__init__()
        self.__browser = browser
        self.__buildingName = buildingName

    def visitInfrastructure(self):
        military = self.__browser.find_element_by_xpath('//a[contains(text(), \'Инфраструктура\') and @class=\'tabItem\']')
        military.click()
        building = self.__browser.find_element_by_xpath('//div[contains(@class, \'buildingWrapper\') and .//*[text()=\'' + self.__buildingName + '\']]')
        build_button = building.find_element_by_css_selector('button.green.new')
        return build_button

    def visitMilitary(self):
        military = self.__browser.find_element_by_xpath('//a[contains(text(), \'Военные\') and @class=\'tabItem\']')
        military.click()
        building = self.__browser.find_element_by_xpath('//div[contains(@class, \'buildingWrapper\') and .//*[text()=\'' + self.__buildingName + '\']]')
        build_button = building.find_element_by_css_selector('button.green.new')
        return build_button

    def visitIndustry(self):
        military = self.__browser.find_element_by_xpath('//a[contains(text(), \'Промышленность\') and @class=\'tabItem\']')
        military.click()
        building = self.__browser.find_element_by_xpath('//div[contains(@class, \'buildingWrapper\') and .//*[text()=\'' + self.__buildingName + '\']]')
        build_button = building.find_element_by_css_selector('button.green.new')
        return build_button