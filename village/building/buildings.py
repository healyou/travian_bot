from abc import abstractmethod
from village.visitors import BuildFieldExceptionVisitor
from exceptions.exceptions import BuildFieldException, BuildFieldExceptionType
from selenium.common.exceptions import NoSuchElementException
import re
from utils.context import Context
from village.types import Production, IndoorBuildingType


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


# Здание внутри деревни
class IndoorBuilding(AbstractBuilding):
    def __init__(self, type: IndoorBuildingType):
        super(IndoorBuilding, self).__init__()
        self._type = type
        self._browser = Context.browser

    def build(self):
        # TODO - новое здание и старое обрабатываются по разному
        # TODO - доделать строительство здания и обработку ошибок
        browser = self._browser
        # надо найти все элементы, потом делать по ним hover и определять, что построено на данном месте
        elems = browser.find_elements_by_css_selector('div#village_map > div.buildingSlot')
        k = 1
        from selenium.webdriver.common.action_chains import ActionChains
        for elem in elems:
            element_to_hover_over = elem
            hover = ActionChains(browser).move_to_element(element_to_hover_over)
            hover.perform()
            # здесь текст основных зданий
            hover_elem_tytle = browser.find_element_by_css_selector('div.tip > div.tip-container > div.tip-contents > div.title.elementTitle')
            # здесь будет текст стройплощадки-пустое место для строительства
            hover_elem_text = browser.find_element_by_css_selector('div.tip > div.tip-container > div.tip-contents > div.text.elementText')
            # print ('title=' + hover_elem_tytle.text + ' text=' + hover_elem_text.text)

            if ('123Стройплощадка' in hover_elem_text.text):
                # по остальным нельзя клинуть - св-во pointer-events: None - только для стройплощадки
                click_item = element_to_hover_over.find_element_by_css_selector('.hoverShapeWinter')
                click_item.click()
                break

            # Получаем текст первого уровня
            all_text = hover_elem_tytle.text
            child_elems = hover_elem_tytle.find_elements_by_xpath("./*")
            parent_text = all_text
            for child in child_elems:
                parent_text = parent_text.replace(child.text, '')
            print ('one_level_text=' + parent_text)
            if ('Главное здание' in parent_text):
                # у построенных зданий можно кликать по самому элементу или по уровню
                click_item = element_to_hover_over.find_element_by_css_selector('.level')
                click_item.click()
                # element_to_hover_over.click()
                break

            # first_lvl_title = hover_elem_tytle.find_elements_by_xpath("./*")
            # for ggwp in first_lvl_title:
            #     print ('flvltitle=' + ggwp.text)
        # village.run()