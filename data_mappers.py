from service_classes import Config
from dto import *

class OrderAssetToOrderHistoryMapper:
    def __init__(self) -> None:
        self.__config = Config()

    def order_assets_to_order_history(self, order_list:Iterable[OrderAssetDTO]) -> OrderHistoryCollection:
        mapped_data = []
        for record in order_list:
            for i in range(len(record.date)): 
                if record.date[i] is None:
                    continue
                mapped_data.append(self.order_asset_to_order_record(record,i))
        return mapped_data

    def order_asset_to_order_record(self, asset:OrderAssetDTO, date_index:int) -> OrderHistoryRecord:
        record = OrderHistoryRecord()
        if asset.status[date_index] in ('New', 'InProgress') or 'Cancel' in asset.status:
            record.px_fill = record.volume_fill = 0
        record.id = asset.id
        record.px_init = asset.px_init
        record.volume_init = asset.volume_init
        record.status = asset.status[date_index]
        record.date = asset.date[date_index]
        record.note = asset.note
        record.tag = asset.tag
        record.side = asset.side
        record.instrument = asset.instrument
        return record
            

class OrderHistoryToDataBaseDTOMapper:
    
    def __init__(self) -> None:
        self.__config = Config()

    def order_history_to_DB_DTO(self, order_history:OrderHistoryCollection) -> Iterable[DataBaseOrderDTO]:
        mapped_data = []
        for record in order_history.order_collection:
            mapped_record = DataBaseOrderDTO()
            hex_id = hex(record.id)
            mapped_record.id = '0'*(10-len(hex_id)) + hex_id
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
            mapped_record.id = int(record.id, 16)
            mapped_record.px_fill = record.px_fill
            mapped_record.px_init = record.px_init
            mapped_record.volume_fill = record.volume_fill
            mapped_record.volume_init = record.volume_init
            mapped_record.status = record.status
            mapped_record.note = record.note
            mapped_record.tag = record.tag
            mapped_record.side = record.side
            mapped_record.instrument = record.instrument
            mapped_record.date = datetime.strptime(record.date, self.__config['date']['db_date_format'])
            mapped_data.append(mapped_record)
        return  OrderHistoryCollection(mapped_data)

