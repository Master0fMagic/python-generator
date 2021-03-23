from service_classes import Config
from factory import ConcreteBuilder, ConcreteFactory

my_config = Config()
factory = ConcreteFactory(builder=ConcreteBuilder())

data = factory.generate_order_history(my_config['ALL_RECORDS'])

last = data[-1]
first = data[0]
print(last)