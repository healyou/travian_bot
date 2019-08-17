from abc import abstractmethod
from enum import Enum
from collections import namedtuple


ProductionTuple = namedtuple('ProductionTuple', ['code', 'displayName'])
class Production(Enum):
    WOOD = ProductionTuple('wood', 'Лесопилка')
    CLAY = ProductionTuple('clay', 'Глиняный карьер')
    IRON = ProductionTuple('iron', 'Железный рудник')
    CORN = ProductionTuple('corn', 'Ферма')

    @property
    def code(self) -> str:
        return self.value.code

    @property
    def displayName(self) -> str:
        return self.value.displayName

    def accept(self, visitor):
        return visitor.visit(self)


class ProductionTypeVisitor(object):
    def visit(self, type: Production):
        ex_method = {
            Production.WOOD: self.visitWood,
            Production.CLAY: self.visitClay,
            Production.IRON: self.visitIron,
            Production.CORN: self.visitCorn,
        }.get(type, self.onIllegalType)
        return ex_method()

    def onIllegalType(self):
        raise Exception('Неизвестный тип ресурсного поля')

    @abstractmethod
    def visitWood(self):
        pass

    @abstractmethod
    def visitClay(self):
        pass

    @abstractmethod
    def visitIron(self):
        pass

    @abstractmethod
    def visitCorn(self):
        pass


# Тип строительства нового здания
NewIndoorBuildingTuple = namedtuple('NewIndoorBuildingTuple', ['code', 'displayName'])
class NewIndoorBuildingType(Enum):
    INFRASTRUCTURE = NewIndoorBuildingTuple('infrastructure', 'Инфраструктура')
    MILITARY = NewIndoorBuildingTuple('Military', 'Военные')
    INDUSTRY = NewIndoorBuildingTuple('Industry', 'Промышленность')

    @property
    def code(self) -> str:
        return self.value.code

    @property
    def displayName(self) -> str:
        return self.value.displayName

    def accept(self, visitor):
        return visitor.visit(self)


class NewIndoorBuildingTypeVisitor(object):
    def visit(self, type: NewIndoorBuildingType):
        ex_method = {
            NewIndoorBuildingType.INFRASTRUCTURE: self.visitInfrastructure,
            NewIndoorBuildingType.MILITARY: self.visitMilitary,
            NewIndoorBuildingType.INDUSTRY: self.visitIndustry
        }.get(type, self.onIllegalType)
        return ex_method()

    def onIllegalType(self):
        raise Exception('Неизвестный тип нового здания')

    @abstractmethod
    def visitInfrastructure(self):
        pass

    @abstractmethod
    def visitMilitary(self):
        pass

    @abstractmethod
    def visitIndustry(self):
        pass


IndoorBuildingTuple = namedtuple('IndoorBuildingTuple', ['code', 'displayName', 'newBuildType'])
class IndoorBuildingType(Enum):
    STOCK = IndoorBuildingTuple('stock', 'Склад', NewIndoorBuildingType.INFRASTRUCTURE)
    GRANARY = IndoorBuildingTuple('granary', 'Амбар', NewIndoorBuildingType.INFRASTRUCTURE)
    RESIDENCE = IndoorBuildingTuple('residence', 'Резиденция', NewIndoorBuildingType.INFRASTRUCTURE)
    HEDGE = IndoorBuildingTuple('hedge', 'Изгородь', NewIndoorBuildingType.MILITARY)
    WORKSHOP = IndoorBuildingTuple('workshop', 'Мастерская', NewIndoorBuildingType.MILITARY)

    @property
    def code(self) -> str:
        return self.value.code

    @property
    def displayName(self) -> str:
        return self.value.displayName

    @property
    def newBuildType(self) -> NewIndoorBuildingType:
        return self.value.newBuildType

    def accept(self, visitor):
        return visitor.visit(self)


class IndoorBuildingTypeVisitor(object):
    def visit(self, type: IndoorBuildingType):
        ex_method = {
            IndoorBuildingType.STOCK: self.visitStock,
            IndoorBuildingType.GRANARY: self.visitGranary,
            IndoorBuildingType.RESIDENCE: self.visitResidence,
            IndoorBuildingType.HEDGE: self.visitHedge,
            IndoorBuildingType.WORKSHOP: self.visitWorkshop,
        }.get(type, self.onIllegalType)
        return ex_method()

    def onIllegalType(self):
        raise Exception('Неизвестный тип здания')

    @abstractmethod
    def visitStock(self):
        pass

    @abstractmethod
    def visitGranary(self):
        pass

    @abstractmethod
    def visitResidence(self):
        pass

    @abstractmethod
    def visitHedge(self):
        pass

    @abstractmethod
    def visitWorkshop(self):
        pass