from math import log
from generators import CurrentDatesGenerator, IDGenerator, NoteGenerator, OldDatesGenerator, PriceFillGenerator, PriceInitInstrumentGenerator, SideGenerator, StatusGenerator, TagGenerator, VolumeFillGenerator, VolumeInitGenerator
from dto import OrderHistoryCollection
from factory import ConcreteFactory, ConcreteBuilder
from data_mappers import OrderAssetToOrderHistoryTransporter

class OrderHistoryIterator:
    def __init__(self, config, logger) -> None:
        self._config = config
        self.__logger = logger
    
    def generate_order_history(self, old_records_amount:int, cur_records_amount:int, new_records_amount:int) -> OrderHistoryCollection:
        order_assets = []
        factory = ConcreteFactory(ConcreteBuilder(
            id_generator=IDGenerator(self._config),
            date_generator=OldDatesGenerator(self._config),
            note_generator=NoteGenerator(self._config),
            price_fill_generator=PriceFillGenerator(self._config),
            price_instrument_generator=PriceInitInstrumentGenerator(self._config),
            side_generator=SideGenerator(self._config),
            status_genearator=StatusGenerator(self._config),
            tag_generator=TagGenerator(self._config),
            volume_fill_generator=VolumeFillGenerator(self._config),
            volume_init_geneartor=VolumeInitGenerator(self._config)
        ), logger=self.__logger)
        for i in range(old_records_amount):
            order_assets.append(factory.generate_order_asset())

        factory.set_builder_date_generator(CurrentDatesGenerator(self._config))
        for i in range(cur_records_amount):
            order_assets.append(factory.generate_order_asset())

        factory.set_builder_date_generator(OldDatesGenerator(self._config))
        for i in range(new_records_amount):
            order_assets.append(factory.generate_order_asset())

        transporter = OrderAssetToOrderHistoryTransporter()
        return transporter.order_assets_to_order_history(order_assets)
