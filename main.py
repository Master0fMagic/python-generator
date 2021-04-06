from math import log
from data_mappers import OrderHistoryToDataBaseDTOMapper
from dto import OrderHistoryCollection
from my_config import Config
from logger import Logger
from repository import IRepository, MySQLRepository
from order_history_iterator import OrderHistoryIterator

class Client(IRepository):
    def __init__(self, repo:IRepository, config, logger) -> None:
        self.__repository = repo
        self.__config = config
        self.__logger = logger

    def generate_collection(self, old_records_amount:int, cur_records_amount:int, new_records_amount:int) -> OrderHistoryCollection:
        iterator = OrderHistoryIterator(self.__config, self.__logger)
        return iterator.generate_order_history(old_records_amount, cur_records_amount, new_records_amount) 

    def save_to_database(self, orders:OrderHistoryCollection) -> None:
        self.__repository.save_to_database(orders)

    def find_by_id(self, id:int) -> OrderHistoryCollection:
        return self.__repository.find_by_id(id)

    def get_all(self) -> OrderHistoryCollection:
        return self.__repository.get_all()


class Programm:
    __config = None
    __loger = None
        
    @staticmethod
    def main():
        Programm.setup()
        client = Client(MySQLRepository(Programm.__config, OrderHistoryToDataBaseDTOMapper(), Programm.__loger), Programm.__config, Programm.__loger)
        data = client.generate_collection(Programm.__config['OLD_RECORDS'], Programm.__config['CURRENT_RECORDS'], Programm.__config['NEW_RECORDS'] )
        for record in data.order_collection:
            print(record)
    
    
    @staticmethod
    def setup():
        Programm.__config = Config()
        Programm.__loger = Logger()



if __name__ == '__main__':
    Programm.main()
    