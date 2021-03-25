from dto import OrderHistoryCollection
from factory import ConcreteFactory, CurrentRecordsBuilder, NewRecordsBuilder, OldRecordsBuilder
from my_config import Config
from data_mappers import OrderAssetToOrderHistoryTransporter

class OrderHistoryCreator:
    def __init__(self) -> None:
        self._config = Config()
    
    def generate_order_history(self, old_records_amount:int, cur_records_amount:int, new_records_amount:int) -> OrderHistoryCollection:
        order_assets = []
        factory = ConcreteFactory(OldRecordsBuilder())
        for i in range(old_records_amount):
            order_assets.append(factory.generate_order_asset())
        factory = ConcreteFactory(CurrentRecordsBuilder())
        for i in range(cur_records_amount):
            order_assets.append(factory.generate_order_asset())
        factory = ConcreteFactory(NewRecordsBuilder())
        for i in range(new_records_amount):
            order_assets.append(factory.generate_order_asset())
        transporter = OrderAssetToOrderHistoryTransporter()
        return transporter.order_assets_to_order_history(order_assets)
