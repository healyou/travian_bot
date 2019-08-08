from abc import abstractmethod
from village.visitors import BuildFieldExceptionVisitor
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from selenium.common.exceptions import NoSuchElementException
import re
from utils.context import Context
from village.types import Production, IndoorBuilding


class AbstractBuilding(object):
    @abstractmethod
    def build(self):
        pass


# Ресурсное поле
class ProductionBuilding(AbstractBuilding):
    def __init__(self, type: Production):
        super(ProductionBuilding, self).__init__()
        self._type = type
        self._browser = Context.browser

    def build(self):
        try:
            self.__tryToBuildField()
        except BuildFieldException as err:
            err.accept(BuildFieldExceptionVisitor())

    def __tryToBuildField(self):
        # Список полей указанного типа
        search_fields = self.__getFieldsForSelectedType(self._type)
        # Определяем поле с наименьшим уровнем для строительства
        field = self.__getFieldWithSmallLevel(search_fields)
        # Собственно строим здание
        self.__buildFieldWithRaiseException(field)

    # Получить элементы всех полей по заданному типу
    def __getFieldsForSelectedType(self, type: Production):
        name_for_search = self.__getFieldNameByBuildingType(type)
        # Информация обо всех полях деревни
        fields = self._browser.find_elements_by_css_selector('div > map#rx > area[shape=\'circle\']')
        search_fields = []
        for field in fields:
            name = field.get_attribute('alt')
            if (name_for_search in name):
                search_fields.append(field)
        return search_fields

    # TODO сделать приватные переменные и протектные в питоне
    # Получить поле с самым маленьким уровнем
    def __getFieldWithSmallLevel(self, search_fields):
        min_lvl_field = None
        min_lvl = None
        for field in search_fields:
            name = field.get_attribute('alt')
            lvl = int(re.findall("\d+", name)[0])
            if (min_lvl is None or min_lvl > lvl):
                min_lvl = lvl
                min_lvl_field = field
        return min_lvl_field

    def __buildFieldWithRaiseException(self, field):
        name = field.get_attribute('alt')
        print ('Попытка построить здание ' + name)
        field.click()
        error_message = ''
        try:
            field = self._browser.find_element_by_css_selector('div.errorMessage > span')
            error_message = field.text
        except NoSuchElementException:
            pass

        if ('Недостаток продовольствия: развивайте фермы' in error_message):
            raise BuildFieldException(error_message, BuildFieldExceptionType.NOT_ENOUGH_FOOD, self)
        else:
            try:
                field = self._browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button.green.build')
                print ('Строительство поля: ' + name)
                field.click()
            except NoSuchElementException:
                raise BuildFieldException('Кнопка строительства недоступна', BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE, self)

    def __getFieldNameByBuildingType(self, type: Production) -> str:
        return {
            Production.WOOD: 'Лесопилка Уровень',
            Production.IRON: 'Железный рудник Уровень',
            Production.CLAY: 'Глиняный карьер Уровень',
            Production.CORN: 'Ферма Уровень'
        }[type]


# Ресурсное поле
class IndoorBuilding(AbstractBuilding):
    def __init__(self, type: IndoorBuilding):
        super(ProductionBuilding, self).__init__()
        self._type = type
        self._browser = Context.browser

    def build(self):
        pass