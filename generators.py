from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from math import ceil, sin
from service_classes import PseudoRandom, Config
from typing import Iterable
from dto import OrderAssetDTO

class IGenerator(metaclass = ABCMeta):
    _orders:Iterable[OrderAssetDTO] = None
    _random_numbers:Iterable[int] = None

    @abstractmethod
    def generate_data(self) -> Iterable[OrderAssetDTO]:
        pass


class TagGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
            self.__config = Config()
            self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['tags'], records_amount, len(self.__config['tags']))
            if orders is None:
                self._orders = [OrderAssetDTO() for i in range(records_amount)]
            else:
                self._orders = orders

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        for i in range(len(self._orders)):
            row_tags = ''
            for j in range(len(self._random_numbers)):
                if self._random_numbers[j][i] % self.__config['tag_divider'] == 0:
                    row_tags += self.__config['tags'][j] + ';'
            self._orders[i].tag = row_tags
        return self._orders
    

class PriceInstrumentGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO]) -> None:
            self.__config = Config()
            self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['price'], records_amount)
            if orders is None:
                self._orders = [OrderAssetDTO() for i in range(records_amount)]
            else:
                self._orders = orders

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        instruments_amount = len(self.__config['instrument'])
        for i in range(len(self._orders)):
            #choosing instrument
            instrument_number = self._random_numbers[i] % instruments_amount
            self._orders[i].instrument = self.__config['instrument'][instrument_number]['quotation']
            self._orders[i].px_init = self.__config['instrument'][instrument_number]['price']
            #generating px_fill
            if self._orders[i].status[2] == self.__config['statuses'][2][2]:  #if status is Cancel
                self._orders[i].px_fill = 0
            else:                                                               #if status is PartilFill
                price_increment = self._random_numbers[i] /PseudoRandom.get_M()
                price_increment = ceil(price_increment*100)
                price_increment *= float(self.__config['instrument'][instrument_number]['min_deviation'])
                if sin(self._random_numbers[i]) < 0:
                    price_increment *= -1
                self._orders[i].px_fill = self._orders[i].px_init + price_increment
        return self._orders


class NoteGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
            self.__config = Config()
            self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['notes'], records_amount)
            if orders is None:
                self._orders = [OrderAssetDTO() for i in range(records_amount)]
            else:
                self._orders = orders
    
    def generate_data(self) -> Iterable[OrderAssetDTO]:
        notes_amount = len(self.__config['notes'])
        for i in range(len(self._orders)):
            self._orders[i].note = self.__config['notes'][self._random_numbers[i] % notes_amount]
        return self._orders


class VolumeSideGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
            self.__config = Config()
            self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['volume'], records_amount, 2)
            if orders is None:
                self._orders = [OrderAssetDTO() for i in range(records_amount)]
            else:
                self._orders = orders

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        side_amount = len(self.__config['sides'])
        for i in range(len(self._orders)):
            #volume init
            self._orders[i].volume_init = (self._random_numbers[0][i]/PseudoRandom.get_M())
            self._orders[i].volume_init*= self.__config['volume']['max'] * 100
            self._orders[i].volume_init = ceil(self._orders[i].volume_init)
            self._orders[i].volume_init /= 100
            self._orders[i].volume_init *= self.__config['volume']['lot_size']
            #volume fill
            if self._orders[i].status[2] == self.__config['statuses'][2][2]:    #if status is Cancel
                self._orders[i].volume_fill = 0
            elif self._orders[i].status[2] == self.__config['statuses'][2][0]:  #if status is Fill
                self._orders[i].volume_fill = self._orders[i].volume_init
            else:                                                               #if status is PartialFill
                max_diff = self._orders[i].volume_init/self.__config['volume']['lot_size'] * self.__config['volume']['max_difference']
                difference = self._random_numbers[1][i] / PseudoRandom.get_M()
                difference *= max_diff
                difference = ceil(difference * 100) /100
                difference *= self.__config['volume']['lot_size']
                self._orders[i].volume_fill = self._orders[i].volume_init - difference
            #side
            self._orders[i].side = self.__config['sides'][self._random_numbers[1][i] % side_amount]
        return self._orders


class IDGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
            self.__config = Config()
            self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['id'], records_amount)
            if orders is None:
                self._orders = [OrderAssetDTO() for i in range(records_amount)]
            else:
                self._orders = orders
    
    def generate_data(self) -> Iterable[OrderAssetDTO]:
        self._orders[0].id = self.__config['first_values']['id']
        for i in range(1,len(self._orders)):
            self._orders[i].id = self._orders[i-1].id + self._random_numbers[i-1]
        return self._orders


class OldDatesGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
        self.__config = Config()
        self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['old_dates'], records_amount, 3)
        if orders is None:
            self._orders = [OrderAssetDTO() for i in range(records_amount)]
        else:
            self._orders = orders

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        first_date = datetime.strptime(self.__config['date']['first_date'], self.__config['date']['config_date_format'])
        for i in range(len(self._orders)):
            for j in range(len(self._random_numbers)):
                time_increment =  (self._random_numbers[j][i] % self.__config['date']['max_date_increment']) / 1000
                time_increment = timedelta(seconds=time_increment)
                if j == 0 and i ==0:
                    self._orders[i].date.append(first_date + time_increment)
                elif j==0:
                    self._orders[i].date.append(self._orders[i-1].date[j] + time_increment)
                else:
                    self._orders[i].date.append(self._orders[i].date[j-1] + time_increment)
        
        for i in range(len(self._orders)):
            for j in range(len(self._random_numbers)):
                if self._random_numbers[0][i] % 5 == 0:
                    self._orders[i].date[0] = None
            
        return self._orders
                

class CurrentDatesGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
        self.__config = Config()
        self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['current_dates'], records_amount, 4)
        if orders is None:
            self._orders = [OrderAssetDTO() for i in range(records_amount)]
        else:
            self._orders = orders

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        first_date = datetime.strptime(self.__config['date']['first_date'], self.__config['date']['config_date_format'])
        for i in range(len(self._orders)):
            for j in range(len(self._random_numbers)):
                time_increment =  (self._random_numbers[j][i] % self.__config['date']['max_date_increment']) / 1000
                time_increment = timedelta(seconds=time_increment)
                if j == 0 and i == 0:
                    self._orders[i].date.append(first_date + time_increment)
                elif j == 0:
                    self._orders[i].date.append(self._orders[i-1].date[j] + time_increment)
                else:
                    self._orders[i].date.append(self._orders[i].date[j-1] + time_increment)
        return self._orders


class NewDatesGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
        self.__config = Config()
        self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['new_dates'], records_amount, 3)
        if orders is None:
            self._orders = [OrderAssetDTO() for i in range(records_amount)]
        else:
            self._orders = orders

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        first_date = datetime.strptime(self.__config['date']['first_new_date'], self.__config['date']['config_date_format'])
        for i in range(len(self._orders)):
            for j in range(len(self._random_numbers)):
                time_increment =  (self._random_numbers[j][i] % self.__config['date']['max_date_increment']) / 1000
                time_increment = timedelta(seconds=time_increment)
                if j == 0 and i == 0:
                    self._orders[i].date.append(first_date + time_increment)
                elif j==0:
                    self._orders[i].date.append(self._orders[i-1].date[j] + time_increment)
                else:
                    self._orders[i].date.append(self._orders[i].date[j-1] + time_increment)
        
        for i in range(len(self._orders)):
            for j in range(len(self._random_numbers)):
                if self._random_numbers[-1][i] % 5 == 0:
                    self._orders[i].date[-1] = None

        return self._orders


class AllDatesGenerator(IGenerator):
    def __init__(self, old_records_amount:int, cur_records_amount:int, new_records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
        self.__config = Config()
        if orders is None:
            self._orders = [OrderAssetDTO() for i in range(old_records_amount + cur_records_amount + new_records_amount)]
        else:
            self._orders = orders
        self.__new_record_amount = new_records_amount
        self.__cur_record_amount = cur_records_amount
        self.__old_record_amount = old_records_amount

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        #getting all dates
        generator = OldDatesGenerator(self.__old_record_amount, self._orders[0:self.__old_record_amount])
        old_dates = generator.generate_data()
        generator = CurrentDatesGenerator(self.__cur_record_amount, self._orders[self.__old_record_amount: self.__old_record_amount + self.__cur_record_amount])
        current_dates = generator.generate_data()
        generator = NewDatesGenerator(self.__new_record_amount, self._orders[self.__old_record_amount + self.__cur_record_amount:])
        new_dates = generator.generate_data()
        
        #formatting some values
        for i in range(len(old_dates)):
            old_dates[i].date.insert(0, None)
        for i in range(len(new_dates)):
            new_dates[i].date.append(None)

        return old_dates + current_dates + new_dates


class StatusGenerator(IGenerator):
    def __init__(self, records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
            self.__config = Config()
            self._random_numbers = PseudoRandom.get_random_list(self.__config['first_values']['third_status'], records_amount)
            if orders is None:
                self._orders = [OrderAssetDTO() for i in range(records_amount)]
            else:
                self._orders = orders

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        third_statuses_amount = len(self.__config['statuses'][2])
        for i in range(len(self._orders)):
            self._orders[i].status = [self.__config['statuses'][0],
                self.__config['statuses'][1],
                self.__config['statuses'][2][self._random_numbers[i] % third_statuses_amount],
                self.__config['statuses'][3] ]
        return self._orders
    
