from datetime import datetime
from typing import Iterable

class OrderHistoryRecord:
    id:int = None
    px_fill:float = None
    px_init:float = None
    volume_init:float = None
    volume_fill:float = None
    status:str = None
    date:datetime = None
    note:str = None
    tag:str = None
    side:str = None
    instrument:str = None

class OrderHistoryCollection:
    _order_collection:Iterable[OrderHistoryRecord] = None

    def __init__(self, order_collection:Iterable[OrderHistoryRecord] ) -> None:
        self._order_collection = order_collection

    @property
    def order_collection(self):
        return self._order_collection

    def find_by_id(self, id:int) -> Iterable[OrderHistoryRecord]:
        filtered_records = []
        for order_record in self._order_collection:
            if order_record.id == id:
                filtered_records.append(order_record)
        return filtered_records

class OrderAssetDTO:
    id:int = None
    px_fill:float = None
    px_init:float = None
    volume_init:float = None
    volume_fill:float = None
    status:Iterable[str] = None
    date:Iterable[datetime] = None
    note:str = None
    tag:str = None
    side:str = None
    instrument:str = None

    def __init__(self) -> None:
        self.status = list()
        self.date = list()
        self.volume_fill = 0
        self.px_fill = 0

class DataBaseOrderDTO:
    id:str = None
    px_fill:float = None
    px_init:float = None
    volume_init:float = None
    volume_fill:float = None
    status:str = None
    date:str = None
    note:str = None
    tag:str = None
    side:str = None
    instrument:str = None