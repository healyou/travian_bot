from dataclasses import dataclass
from datetime import datetime


# Свойства строительства в деревне
@dataclass
class VillageBuildProperties:
    # Автоматическое строительство ресурсов
    auto_build_resources: bool
    # Время строительства следующего здания
    next_build_datetime: datetime
    # Необходимость строительства склада или амбара
    # None - ничего, True - Stock, False - Granary
    is_stock_or_granary_build: bool


@dataclass
class Point:
    x: int
    y: int


# Данные деревни
@dataclass
class VillageData:
    prop: VillageBuildProperties
    point: Point


@dataclass
class VillageInfo:
    name: str
    point: Point


@dataclass
class BuildVillageInfo:
    info: VillageInfo
    auto_build_res: bool


@dataclass
class BuildProperties:
    # Автоматическое строительство ресурсов
    info_list: list