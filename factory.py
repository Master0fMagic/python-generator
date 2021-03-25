from abc import ABCMeta, abstractmethod
from logger import Logger
from generators import *
from typing import Iterable
from dto import OrderAssetDTO, OrderHistoryCollection


class IBuilder(metaclass=ABCMeta):
    
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
    def build_price_init_instruments(self) -> None:
        pass

    @abstractmethod
    def build_price_fill(self) -> None:
        pass

    @abstractmethod
    def build_volume_init(self) -> None:
        pass

    @abstractmethod
    def build_volume_fill(self) -> None:
        pass

    @abstractmethod
    def build_side(self) -> None:
        pass

    @abstractmethod
    def build_tags(self) -> None:
        pass

    @abstractmethod
    def build_notes(self) -> None:
        pass

    @abstractmethod
    def get_result(self) -> OrderAssetDTO:
        pass


class IFactory(metaclass=ABCMeta):
    @abstractmethod
    def generate_order_asset(self) -> OrderAssetDTO:
        pass


class OldRecordsBuilder(IBuilder):
    def __init__(self) -> None:
        self.__orderAsset = OrderAssetDTO() 

    def reset(self) -> None:
        self.__orderAsset = None      
        
    def get_result(self) -> OrderAssetDTO:
        return self.__orderAsset
    
    def build_dates(self) -> None:
        generator = OldDatesGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_id(self) -> None:
        generator = IDGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_statuses(self) -> None:
        generator = StatusGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_notes(self) -> None:
        generator = NoteGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_price_init_instruments(self) -> None:
        generator = PriceInitInstrumentGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_volume_init(self) -> None:
        generator = VolumeInitGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_price_fill(self) -> None:
        generator = PriceFillGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_volume_fill(self) -> None:
        generator = VolumeFillGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_side(self) -> None:
        generator = SideGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_tags(self) -> None:
        generator = TagGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()


class CurrentRecordsBuilder(IBuilder):
       
    def __init__(self) -> None:
        self.__orderAsset = OrderAssetDTO() 

    def reset(self) -> None:
        self.__orderAsset = None
        
    def get_result(self) -> OrderAssetDTO:
        return self.__orderAsset
    
    def build_dates(self) -> None:
        generator = CurrentDatesGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_id(self) -> None:
        generator = IDGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_statuses(self) -> None:
        generator = StatusGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_notes(self) -> None:
        generator = NoteGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_price_init_instruments(self) -> None:
        generator = PriceInitInstrumentGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_volume_init(self) -> None:
        generator = VolumeInitGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_price_fill(self) -> None:
        generator = PriceFillGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_volume_fill(self) -> None:
        generator = VolumeFillGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_side(self) -> None:
        generator = SideGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_tags(self) -> None:
        generator = TagGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()
        

class NewRecordsBuilder(IBuilder):
       
    def __init__(self) -> None:
        self.__orderAsset = OrderAssetDTO()

    def reset(self) -> None:
        self.__orderAsset = None         
        
    def get_result(self) -> OrderAssetDTO:
        return self.__orderAsset
    
    def build_dates(self) -> None:
        generator = NewDatesGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_id(self) -> None:
        generator = IDGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_statuses(self) -> None:
        generator = StatusGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_notes(self) -> None:
        generator = NoteGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_price_init_instruments(self) -> None:
        generator = PriceInitInstrumentGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_volume_init(self) -> None:
        generator = VolumeInitGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_price_fill(self) -> None:
        generator = PriceFillGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_volume_fill(self) -> None:
        generator = VolumeFillGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_side(self) -> None:
        generator = SideGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()

    def build_tags(self) -> None:
        generator = TagGenerator(self.__orderAsset)
        self.__orderAsset = generator.generate_data()
        

class ConcreteFactory(IFactory):
    def __init__(self, builder:IBuilder) -> None:
        self.__builder = builder
        self.__logger = Logger()
    
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

