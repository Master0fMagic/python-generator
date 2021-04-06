from abc import ABCMeta, abstractmethod
from logger import Logger
from generators import *
from typing import Generator, Iterable
from dto import OrderAssetDTO, OrderHistoryCollection


class IFactory(metaclass=ABCMeta):
    @abstractmethod
    def generate_order_asset(self) -> OrderAssetDTO:
        pass

    @abstractmethod
    def set_builder_date_generator(self, date_generator:IGenerator):
        pass


class ConcreteBuilder:
    def __init__(self, id_generator:IGenerator, date_generator:IGenerator, status_genearator:IGenerator, note_generator:IGenerator, 
    price_instrument_generator:IGenerator, volume_init_geneartor:IGenerator, price_fill_generator:IGenerator, volume_fill_generator:IGenerator,
    side_generator:IGenerator, tag_generator:IGenerator) -> None:
        self.__orderAsset = OrderAssetDTO() 
        self.__id_generator = id_generator
        self.__date_generator = date_generator
        self.__status_generator = status_genearator
        self.__note_generator = note_generator
        self.__price_instrument_generator = price_instrument_generator
        self.__volume_init_generator = volume_init_geneartor
        self.__price_fill_generator = price_fill_generator
        self.__volume_fill_generator = volume_fill_generator
        self.__side_generator = side_generator
        self.__tag_generator = tag_generator


    def set_date_generator(self, date_generator:IGenerator):
        self.__date_generator = date_generator

    def reset(self) -> None:
        self.__orderAsset = OrderAssetDTO()      
        
    def get_result(self) -> OrderAssetDTO:
        return self.__orderAsset
    
    def build_dates(self) -> None:
        self.__date_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__date_generator.generate_data()

    def build_id(self) -> None:
        self.__id_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__id_generator.generate_data()

    def build_statuses(self) -> None:
        self.__status_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__status_generator.generate_data()

    def build_notes(self) -> None:
        self.__note_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__note_generator.generate_data()

    def build_price_init_instruments(self) -> None:
        self.__price_instrument_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__price_instrument_generator.generate_data()

    def build_volume_init(self) -> None:
        self.__volume_init_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__volume_init_generator.generate_data()

    def build_price_fill(self) -> None:
        self.__price_fill_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__price_fill_generator.generate_data()

    def build_volume_fill(self) -> None:
        self.__volume_fill_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__volume_fill_generator.generate_data()

    def build_side(self) -> None:
        self.__side_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__side_generator.generate_data()

    def build_tags(self) -> None:
        self.__tag_generator.set_asset(self.__orderAsset)
        self.__orderAsset = self.__tag_generator.generate_data()
      

class ConcreteFactory(IFactory):
    def __init__(self, builder:ConcreteBuilder, logger) -> None:
        self.__builder = builder
        self.__logger = logger
    
    def set_builder_date_generator(self, date_generator:IGenerator):
        self.__builder.set_date_generator(date_generator)

    def generate_order_asset(self) -> OrderAssetDTO:
        self.__builder.reset()
        self.__builder.build_id()
        self.__builder.build_dates()
        self.__builder.build_statuses()
        self.__builder.build_price_init_instruments()
        self.__builder.build_price_fill()
        self.__builder.build_volume_init()
        self.__builder.build_volume_fill()
        self.__builder.build_side()
        self.__builder.build_tags()
        self.__builder.build_notes()
        #self.__logger.info(f'Order genereted')
        return self.__builder.get_result()

