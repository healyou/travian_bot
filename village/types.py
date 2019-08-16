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


IndoorBuildingTuple = namedtuple('IndoorBuildingTuple', ['code', 'displayName'])
class IndoorBuildingType(Enum):
    STOCK = IndoorBuildingTuple('stock', 'Склад')
    GRANARY = IndoorBuildingTuple('granary', 'Амбар')
    RESIDENCE = IndoorBuildingTuple('residence', 'Резиденция')
    HEDGE = IndoorBuildingTuple('hedge', 'Изгородь')
    WORKSHOP = IndoorBuildingTuple('workshop', 'Мастерская')

    @property
    def code(self) -> str:
        return self.value.code

    @property
    def displayName(self) -> str:
        return self.value.displayName

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