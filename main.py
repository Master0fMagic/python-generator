from dto import OrderHistoryCollection
from service_classes import Config, DBService
from factory import ConcreteBuilder, ConcreteFactory, IFactory
from repository import IRepository, MySQLRepository

class Client(IRepository):
    def __init__(self, repo:IRepository) -> None:
        self.__repository = repo

    def generate_collection(self, factory:IFactory, amount:int) -> OrderHistoryCollection:
        data = factory.generate_order_history(amount)
        return data

    def save_to_database(self, orders:OrderHistoryCollection) -> None:
        self.__repository.save_to_database(orders)

    def find_by_id(self, id:int) -> OrderHistoryCollection:
        return self.__repository.find_by_id(id)

    def get_all(self) -> OrderHistoryCollection:
        return self.__repository.get_all()


if __name__ == '__main__':
    my_config = Config()
    client = Client(MySQLRepository())
    #data = client.generate_collection(ConcreteFactory(builder=ConcreteBuilder()), my_config['ALL_RECORDS'] )
    data = client.find_by_id(68773968890)
    for record in data.order_collection:
        print(record)
    