from abc import ABCMeta, abstractmethod

class IRepository(metaclass = ABCMeta):
    pass

class MySQLRepository(IRepository):
    pass