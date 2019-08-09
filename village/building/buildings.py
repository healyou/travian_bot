from abc import abstractmethod
from village.visitors import BuildFieldExceptionVisitor
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from selenium.common.exceptions import NoSuchElementException
import re
from utils.context import Context
from village.types import Production, IndoorBuildingType
from selenium.webdriver.common.action_chains import ActionChains


# TODO - это надо вынести в отдельный метод для строительства не нового здания
def buildFieldWithRaiseException(browser, name: str):
    print ('Попытка построить ' + name)
    error_message = ''
    try:
        field = browser.find_element_by_css_selector('div.errorMessage > span')
        error_message = field.text
    except NoSuchElementException:
        pass

    if ('Недостаток продовольствия: развивайте фермы' in error_message):
        raise BuildFieldException(error_message, BuildFieldExceptionType.NOT_ENOUGH_FOOD)
    else:
        try:
            field = browser.find_element_by_css_selector('.upgradeButtonsContainer > .section1 > button.green.build')
            print ('Строительство: ' + name)
            # field.click()
        except NoSuchElementException:
            raise BuildFieldException('Кнопка строительства недоступна', BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE)


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
        buildFieldWithRaiseException(self._browser, name)

    def __getFieldNameByBuildingType(self, type: Production) -> str:
        return {
            Production.WOOD: 'Лесопилка Уровень',
            Production.IRON: 'Железный рудник Уровень',
            Production.CLAY: 'Глиняный карьер Уровень',
            Production.CORN: 'Ферма Уровень'
        }[type]


# Здание внутри деревни
class IndoorBuilding(AbstractBuilding):
    def __init__(self, type: IndoorBuildingType):
        super(IndoorBuilding, self).__init__()
        self._type = type
        self._browser = Context.browser

    def build(self):
        try:
            self.__tryToBuildField()
        except BuildFieldException as err:
            err.accept(BuildFieldExceptionVisitor())
    
    # TODO - рефактор
    def __tryToBuildField(self):
        # TODO - новое здание и старое обрабатываются по разному
        # TODO - доделать строительство здания и обработку ошибок
        browser = self._browser
        # надо найти все элементы, потом делать по ним hover и определять, что построено на данном месте

        # TODO - находит блоки, на которые не нажать - надо искать с уровнем и на него кликать
        elems = browser.find_elements_by_css_selector('div#village_map > div.buildingSlot')
        k = 1

        build_clicked_field = None
        name = None
        first_empty_clicked_field = None
        for elem in elems:
            element_to_hover_over = elem
            print (element_to_hover_over.get_attribute('innerHTML'))
            print ('')
            hover = ActionChains(browser).move_to_element(element_to_hover_over)
            hover.perform()
            # здесь текст основных зданий
            hover_elem_tytle = browser.find_element_by_css_selector('div.tip > div.tip-container > div.tip-contents > div.title.elementTitle')
            # здесь будет текст стройплощадки-пустое место для строительства
            hover_elem_text = browser.find_element_by_css_selector('div.tip > div.tip-container > div.tip-contents > div.text.elementText')
            # print ('title=' + hover_elem_tytle.text + ' text=' + hover_elem_text.text)

            if ('Стройплощадка' in hover_elem_text.text and first_empty_clicked_field is None):
                # по остальным нельзя клинуть - св-во pointer-events: None - только для стройплощадки
                click_item = element_to_hover_over.find_element_by_css_selector('.hoverShapeWinter')
                first_empty_clicked_field = click_item
                print ('Найдено пустое поле для строительства')
                continue

            # Получаем текст первого уровня
            all_text = hover_elem_tytle.text
            child_elems = hover_elem_tytle.find_elements_by_xpath("./*")
            parent_text = all_text
            for child in child_elems:
                parent_text = parent_text.replace(child.text, '')
            print ('one_level_text=' + parent_text)

            if (self._type == IndoorBuildingType.Stock):
                if ('Склад' in parent_text):
                    click_item = element_to_hover_over.find_element_by_css_selector('.level')
                    build_clicked_field = click_item
                    name = 'Склад'
                    break
            elif (self._type == IndoorBuildingType.GRANARY):
                if ('Амбар' in parent_text):
                    click_item = element_to_hover_over.find_element_by_css_selector('.level')
                    build_clicked_field = click_item
                    name = 'Амбар'
                    break
            elif (self._type == IndoorBuildingType.HEDGE):
                if ('Изгородь' in parent_text):
                    click_item = element_to_hover_over.find_element_by_css_selector('.level')
                    build_clicked_field = click_item
                    name = 'Изгородь'
                    break
            # TODO - другие здания для постройки

        if (build_clicked_field is not None):
            print ('Строим ' + name)
            build_clicked_field.click()
            buildFieldWithRaiseException(self._browser, name)
        else:
            print ('Надо строить новое здание')
            if (first_empty_clicked_field is None):
                raise BuildFieldException('Нет места для строительства здания', BuildFieldExceptionType.NOT_ENOUGH_PLACE)
            else:
                # TODO - надо выбирать здание из 3 типов - пром, военные и инфраструктура
                first_empty_clicked_field.click()

                military = self._browser.find_element_by_xpath('//a[contains(text(), \'Военные\') and @class=\'tabItem\']')
                military.click()

                # TODO - тут можно строить и другие типы зданий
                if (self._type == IndoorBuildingType.HEDGE):
                    try:
                        hedge = self._browser.find_element_by_xpath('//div[contains(@class, \'buildingWrapper\') and .//*[text()=\'Изгородь\']]')
                        build_hedge = hedge.find_element_by_css_selector('button.green.new')
                        print ('Строим изгородь')
                        build_hedge.click()
                    except NoSuchElementException as err:
                        raise BuildFieldException('Кнопка строительства недоступна', BuildFieldExceptionType.BUILD_BUTTON_UNAVAILABLE)