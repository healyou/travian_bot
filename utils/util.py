import os
import re


# Получает из строки с ascii символами число
def convert_str_with_one_number_to_int(s):
    utf = s.encode('ascii', 'ignore').decode('UTF-8')
    str = utf.replace(' ', '')
    numStr = re.findall('\d+', str)[0]
    return int(numStr)


def getVillagesCoords(browser):
    coord = []

    css = '#sidebarBoxVillagelist > .sidebarBoxInnerBox > .content > ul > li'
    elems = browser.find_elements_by_css_selector(css)
    for elem in elems:
        # Координаты деревни
        xComp = elem.find_element_by_css_selector('.coordinates > .coordinateX')
        yComp = elem.find_element_by_css_selector('.coordinates > .coordinateY')
        vilX = convert_str_with_one_number_to_int(xComp.text)
        vilY = convert_str_with_one_number_to_int(yComp.text)
        coord.append((vilX, vilY))

    return coord


def getVillagesInfo(browser):
    villages_info = []

    css = '#sidebarBoxVillagelist > .sidebarBoxInnerBox > .content > ul > li'
    elems = browser.find_elements_by_css_selector(css)
    for elem in elems:
        # Координаты деревни
        xComp = elem.find_element_by_css_selector('.coordinates > .coordinateX')
        yComp = elem.find_element_by_css_selector('.coordinates > .coordinateY')
        vilX = convert_str_with_one_number_to_int(xComp.text)
        vilY = convert_str_with_one_number_to_int(yComp.text)

        from command.queue.properties import VillageInfo
        from command.queue.properties import Point
        coord = Point(vilX, vilY)

        # Наименование деревни
        name_comp = elem.find_element_by_css_selector('div.name')
        name: str = name_comp.text

        info: VillageInfo = VillageInfo(name, coord)
        villages_info.append(info)

    return villages_info


def get_absolute_file_path(cur_script_file, rel_file_path):
    script_dir = os.path.dirname(cur_script_file)
    return os.path.join(script_dir, rel_file_path)


def get_travian_command_files():
    return [
        'files/travian/login.json',
        # 'files/travian/open_village.json',
        # 'files/travian/open_map.json',
        # 'files/travian/open_resources.json'
    ]
