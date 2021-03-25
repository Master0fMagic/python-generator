from dto import OrderHistoryCollection
from my_config import Config
from db_connection import DBService
from logger import Logger
from repository import IRepository, MySQLRepository
from order_history_creator import OrderHistoryCreator

class Client(IRepository):
    def __init__(self, repo:IRepository) -> None:
        self.__repository = repo

    def generate_collection(self, old_records_amount:int, cur_records_amount:int, new_records_amount:int) -> OrderHistoryCollection:
        creator = OrderHistoryCreator()
        return creator.generate_order_history(old_records_amount, cur_records_amount, new_records_amount) 

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
        client = Client(MySQLRepository())
        data = client.generate_collection(Programm.__config['OLD_RECORDS'], Programm.__config['CURRENT_RECORDS'], Programm.__config['NEW_RECORDS'] )
        for record in data.order_collection:
            print(record)
    
    
    @staticmethod
    def setup():
        Programm.__config = Config()
        Programm.__loger = Logger()



if __name__ == '__main__':
    Programm.main()
    