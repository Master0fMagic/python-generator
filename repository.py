from abc import ABCMeta, abstractmethod
from typing import Iterable
from service_classes import Config, DBService, Logger
from dto import DataBaseOrderDTO, OrderHistoryCollection
from data_mappers import OrderHistoryToDataBaseDTOMapper
from id_hex_mapper import IdHexMapper

class IRepository(metaclass = ABCMeta):
    @abstractmethod
    def save_to_database(self, orders:OrderHistoryCollection) -> None:
        pass

    @abstractmethod
    def get_all(self) -> OrderHistoryCollection:
        pass

    @abstractmethod
    def find_by_id(self, id:int) -> OrderHistoryCollection:
        pass


class MySQLRepository(IRepository):
    
    def __init__(self) -> None:
        self.__config = Config()
        self.__mapper = OrderHistoryToDataBaseDTOMapper()
        self.__logger = Logger()
    
    def save_to_database(self, orders: OrderHistoryCollection) -> None:
        orders_dto_collection = self.__mapper.order_history_to_DB_DTO(orders)
        connection = DBService()     
        cursor = connection.cursor()
        query = self.__config['insert_query_template']
        for i in range(len(orders.order_collection)):
            query += self.__config['insert_values_template'].format(
                orders_dto_collection[i].id,
                orders_dto_collection[i].instrument,
                orders_dto_collection[i].px_init,
                orders_dto_collection[i].px_fill,
                orders_dto_collection[i].side,
                orders_dto_collection[i].volume_init,
                orders_dto_collection[i].volume_fill,
                orders_dto_collection[i].date,
                orders_dto_collection[i].status,
                orders_dto_collection[i].note,
                orders_dto_collection[i].tag
            ) + ','
            if i % self.__config['batch_size'] == 0 and i != 0:
                query = query[:-1]
                cursor.execute(query)
                connection.commit()
                query = self.__config['insert_query_template']
        cursor.close()
        self.__logger.info(f'Saved to database {len(orders.order_collection)} order history records')


    def _get_response(self, query:str) -> Iterable[DataBaseOrderDTO]:
        response = []
        cursor = None
        try:
            cursor = DBService().cursor()
            cursor.execute(query)
        except Exception as ex:
            self.__logger.error(f'Error while executing query: {ex}')
        
        for item in cursor:
            order_record = DataBaseOrderDTO()
            order_record.id = item[1]
            order_record.instrument = item[2]
            order_record.px_init = float (item[3] )
            order_record.px_fill = float(item[4])
            order_record.side = item[5]
            order_record.volume_init = float(item[6])
            order_record.volume_fill = float(item[7])
            order_record.date = item[8]
            order_record.status = item[9]
            order_record.note = item[10]
            order_record.tag = item[11]
            response.append(order_record)
        cursor.close()
        return response

    def find_by_id(self, id: int) -> OrderHistoryCollection:
        query = "SELECT * FROM orders_history WHERE OrderNumber = '{}'".format(IdHexMapper.id_to_hex_string(id))
        response = self._get_response(query)
        self.__logger.info(f'Get order history records by id: [{len(response)}] rows')
        return self.__mapper.DB_DTO_to_order_history(response)
    
    def get_all(self) -> OrderHistoryCollection:
        query = "SELECT * FROM orders_history;"
        response = self._get_response(query)
        self.__logger.info(f'Get order history records: [{len(response)}] rows')
        return self.__mapper.DB_DTO_to_order_history(response)
