from abc import ABCMeta, abstractmethod
from data_mappers import OrderAssetToOrderHistoryMapper
from service_classes import Config
from generators import *
from typing import Iterable
from dto import OrderAssetDTO, OrderHistoryCollection


class IBuilder(metaclass=ABCMeta):
    
    @abstractmethod
    def init(self, amount:int) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def build_id(self) -> None:
        pass

    @abstractmethod
    def build_dates(self) -> None:
        pass

    @abstractmethod
    def build_statuses(self) -> None:
        pass

    @abstractmethod
    def build_price_instruments(self) -> None:
        pass

    @abstractmethod
    def build_volumes_side(self) -> None:
        pass

    @abstractmethod
    def build_tags(self) -> None:
        pass

    @abstractmethod
    def build_notes(self) -> None:
        pass

    @abstractmethod
    def get_result(self) -> Iterable[OrderAssetDTO]:
        pass

class IFactory(metaclass=ABCMeta):
    @abstractmethod
    def generate_order_history(self, amount:int, builder:IBuilder) -> OrderHistoryCollection:
        pass

class ConcreteBuilder(IBuilder):
       
    def __init__(self) -> None:
        self.__config = Config()

    def reset(self) -> None:
        self.__orders = None
    
    def init(self, amount:int) -> None:
        self.__orders = [OrderAssetDTO() for i in range(amount)]
        
    def get_result(self) -> Iterable[OrderAssetDTO]:
        return self.__orders
    
    def build_dates(self) -> None:
        generator = AllDatesGenerator(self.__config['OLD_RECORDS'], self.__config['CURRENT_RECORDS'], self.__config['NEW_RECORDS'], self.__orders)
        self.__orders = generator.generate_data()

    def build_id(self) -> None:
        generator = IDGenerator(len(self.__orders), self.__orders)
        self.__orders = generator.generate_data()

    def build_statuses(self) -> None:
        generator = StatusGenerator(len(self.__orders), self.__orders)
        self.__orders = generator.generate_data()

    def build_price_instruments(self) -> None:
        generator = PriceInstrumentGenerator(len(self.__orders), self.__orders)
        self.__orders = generator.generate_data()

    def build_volumes_side(self) -> None:
        generator = VolumeSideGenerator(len(self.__orders), self.__orders)
        self.__orders = generator.generate_data()

    def build_tags(self) -> None:
        generator = TagGenerator(len(self.__orders), self.__orders)
        self.__orders = generator.generate_data()

    def build_notes(self) -> None:
        generator = NoteGenerator(len(self.__orders), self.__orders)
        self.__orders = generator.generate_data()
        

class ConcreteFactory(IFactory):
    def __init__(self, builder:IBuilder) -> None:
        self.__builder = builder
    
    def generate_order_history(self, amount:int) -> OrderHistoryCollection:
        self.__builder.reset()
        self.__builder.init(amount)
        self.__builder.build_id()
        self.__builder.build_dates()
        self.__builder.build_statuses()
        self.__builder.build_price_instruments()
        self.__builder.build_volumes_side()
        self.__builder.build_tags()
        self.__builder.build_notes()

        mapper = OrderAssetToOrderHistoryMapper()
        return mapper.order_assets_to_order_history(self.__builder.get_result())

