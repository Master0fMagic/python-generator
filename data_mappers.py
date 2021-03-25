from my_config import Config
from dto import *
from id_hex_mapper import IdHexMapper

class OrderAssetToOrderHistoryTransporter:

    def order_assets_to_order_history(self, order_list:Iterable[OrderAssetDTO]) -> OrderHistoryCollection:
        order_history_records = []
        for record in order_list:
            order_history_records += self.order_asset_to_order_record(record)
        return OrderHistoryCollection(order_history_records)

    def order_asset_to_order_record(self, asset:OrderAssetDTO) -> Iterable[OrderHistoryRecord]:
        order_history_records = []
        
        for i in range(4):
            record = OrderHistoryRecord()
            if len(asset.date) == 0:
                record.date = None
            elif asset.date[i] is None:
                continue
            else:
                record.date = asset.date[i]

            if asset.status[i] in ('New', 'InProgress') or 'Cancel' in asset.status:
                record.px_fill = record.volume_fill = 0
            else:
                record.px_fill = asset.px_fill
                record.volume_fill = asset.volume_fill

            record.id = asset.id
            record.px_init = asset.px_init
            record.volume_init = asset.volume_init
            record.status = asset.status[i]
            
            record.note = asset.note
            record.tag = asset.tag
            record.side = asset.side
            record.instrument = asset.instrument
            order_history_records.append(record)
        return order_history_records
            

class OrderHistoryToDataBaseDTOMapper:
    
    def __init__(self) -> None:
        self.__config = Config()


    def order_history_to_DB_DTO(self, order_history:OrderHistoryCollection) -> Iterable[DataBaseOrderDTO]:
        mapped_data = []
        for record in order_history.order_collection:
            mapped_record = DataBaseOrderDTO()
            mapped_record.id = IdHexMapper.id_to_hex_string(record.id)
            mapped_record.px_fill = record.px_fill
            mapped_record.px_init = record.px_init
            mapped_record.volume_fill = record.volume_fill
            mapped_record.volume_init = record.volume_init
            mapped_record.status = record.status
            mapped_record.note = record.note
            mapped_record.tag = record.tag
            mapped_record.side = record.side
            mapped_record.instrument = record.instrument
            mapped_record.date = record.date.strftime(self.__config['date']['db_date_format'])[0:-3]
            mapped_data.append(mapped_record)
        return mapped_data


    def DB_DTO_to_order_history(self, order_history:Iterable[DataBaseOrderDTO]) -> OrderHistoryCollection:
        mapped_data = []
        for record in order_history:
            mapped_record = OrderHistoryRecord()
            mapped_record.id = IdHexMapper.hex_id_to_int(record.id)
            mapped_record.px_fill = record.px_fill
            mapped_record.px_init = record.px_init
            mapped_record.volume_fill = record.volume_fill
            mapped_record.volume_init = record.volume_init
            mapped_record.status = record.status
            mapped_record.note = record.note
            mapped_record.tag = record.tag
            mapped_record.side = record.side
            mapped_record.instrument = record.instrument
            if isinstance(record.date, datetime):
                mapped_record.date = record.date
            else:
                mapped_record.date = datetime.strptime(record.date, self.__config['date']['db_date_format'])
            mapped_data.append(mapped_record)
        return  OrderHistoryCollection(mapped_data)

