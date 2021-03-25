from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from math import ceil, sin
from my_config import Config
from pseudo_random import PseudoRandom
from typing import Iterable
from dto import OrderAssetDTO

class IGenerator(metaclass = ABCMeta):
    _orderAsset:OrderAssetDTO = None
    _last_random:int = None

    @abstractmethod
    def generate_data(self) -> OrderAssetDTO:
        pass


class TagGenerator(IGenerator):
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            self._random_amount = len(self.__config['tags'])
            self._step = self.__config['ALL_RECORDS']
            
            if TagGenerator._last_random is None:
                TagGenerator._last_random = self.__config['first_values']['tags']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset

    def generate_data(self) -> OrderAssetDTO:
        random_numbers = PseudoRandom.get_random_list(TagGenerator._last_random, self._random_amount, self._step)
        TagGenerator._last_random = random_numbers[0]

        row_tags = ''
        for j in range(len(random_numbers)):
            if random_numbers[j] % self.__config['tag_divider'] == 0:
                row_tags += self.__config['tags'][j] + ';'
        self._orderAsset.tag = row_tags
        return self._orderAsset
    

class PriceInitInstrumentGenerator(IGenerator):
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            
            if PriceInitInstrumentGenerator._last_random is None:
                PriceInitInstrumentGenerator._last_random = self.__config['first_values']['price']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset

    def generate_data(self) -> OrderAssetDTO:
        if self._orderAsset.px_init != None:
            return self._orderAsset

        random_number = PriceInitInstrumentGenerator._last_random = PseudoRandom.get_random(PriceInitInstrumentGenerator._last_random)
        #choosing instrument
        instrument_number = random_number % len(self.__config['instrument'])
        self._orderAsset.instrument = self.__config['instrument'][instrument_number]['quotation']
        self._orderAsset.px_init = self.__config['instrument'][instrument_number]['price']
        
        return self._orderAsset


class PriceFillGenerator(IGenerator):
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            
            if PriceFillGenerator._last_random is None:
                PriceFillGenerator._last_random = self.__config['first_values']['price']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset

    def generate_data(self) -> OrderAssetDTO:
        if self._orderAsset.px_init is None:
            generator = PriceInitInstrumentGenerator()
            self._orderAsset = generator.generate_data()
        
        random_number = PriceFillGenerator._last_random = PseudoRandom.get_random(PriceFillGenerator._last_random)
        instrument_number = random_number % len(self.__config['instrument'])

        if len(self._orderAsset.status) == 0:
            statusGenerator = StatusGenerator(self._orderAsset)
            self._orderAsset = statusGenerator.generate_data()
        
        if self._orderAsset.status[2] == self.__config['statuses'][2][2]:  #if status is Cancel
            self._orderAsset.px_fill = 0
        else:                                                               #if status is PartilFill
            price_increment = random_number /PseudoRandom.get_M()
            price_increment = ceil(price_increment*100)
            price_increment *= float(self.__config['instrument'][instrument_number]['min_deviation'])
            if sin(random_number) < 0:
                price_increment *= -1
            self._orderAsset.px_fill = self._orderAsset.px_init + price_increment
        return self._orderAsset


class NoteGenerator(IGenerator):
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            
            if NoteGenerator._last_random is None:
                NoteGenerator._last_random = self.__config['first_values']['notes']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset
  
    def generate_data(self) -> OrderAssetDTO:
        random_number = NoteGenerator._last_random = PseudoRandom.get_random(NoteGenerator._last_random)
        self._orderAsset.note = self.__config['notes'][random_number % len(self.__config['notes'])]
        return self._orderAsset


class VolumeInitGenerator(IGenerator):
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            
            if VolumeInitGenerator._last_random is None:
                VolumeInitGenerator._last_random = self.__config['first_values']['volume']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset

    def generate_data(self) -> OrderAssetDTO:
        if self._orderAsset.volume_init != None:
            return self._orderAsset
        
        random_number = VolumeInitGenerator._last_random = PseudoRandom.get_random(VolumeInitGenerator._last_random)
                
        #volume init
        self._orderAsset.volume_init = (random_number/PseudoRandom.get_M())
        self._orderAsset.volume_init*= self.__config['volume']['max'] * 100
        self._orderAsset.volume_init = ceil(self._orderAsset.volume_init)
        self._orderAsset.volume_init /= 100
        self._orderAsset.volume_init *= self.__config['volume']['lot_size']
        
        return self._orderAsset


class VolumeFillGenerator(IGenerator):
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            
            if VolumeFillGenerator._last_random is None:
                VolumeFillGenerator._last_random = PseudoRandom.get_random_with_step(self.__config['first_values']['volume'], self.__config['ALL_RECORDS'])
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset

    def generate_data(self) -> OrderAssetDTO:
        if self._orderAsset.volume_init is None:
            generator = VolumeInitGenerator()
            self._orderAsset = generator.generate_data()
        
        random_number = VolumeFillGenerator._last_random =PseudoRandom.get_random(VolumeFillGenerator._last_random)
        
        if len(self._orderAsset.status) == 0:
            statusGenerator = StatusGenerator(self._orderAsset)
            self._orderAsset = statusGenerator.generate_data()

        if self._orderAsset.status[2] == self.__config['statuses'][2][2]:    #if status is Cancel
            self._orderAsset.volume_fill = 0
        elif self._orderAsset.status[2] == self.__config['statuses'][2][0]:  #if status is Fill
            self._orderAsset.volume_fill = self._orderAsset.volume_init
        else:                                                               #if status is PartialFill
            max_diff = self._orderAsset.volume_init/self.__config['volume']['lot_size'] * self.__config['volume']['max_difference']
            difference = random_number / PseudoRandom.get_M()
            difference *= max_diff
            difference = ceil(difference * 100) /100
            difference *= self.__config['volume']['lot_size']
            self._orderAsset.volume_fill = self._orderAsset.volume_init - difference
        return self._orderAsset


class SideGenerator(IGenerator):
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
        self.__config = Config()
        
        if SideGenerator._last_random is None:
            SideGenerator._last_random = PseudoRandom.get_random_with_step(self.__config['first_values']['volume'], self.__config['ALL_RECORDS'])
        
        if orderAsset is None:
            self._orderAsset = OrderAssetDTO()
        else:
            self._orderAsset = orderAsset
    
    def generate_data(self) -> OrderAssetDTO:
        random_number = SideGenerator._last_random = PseudoRandom.get_random(SideGenerator._last_random)
        self._orderAsset.side = self.__config['sides'][random_number % len(self.__config['sides'])]
        return self._orderAsset


class IDGenerator(IGenerator):
    _last_id = None

    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
        self.__config = Config()
        
        if IDGenerator._last_random is None:
            IDGenerator._last_random = self.__config['first_values']['id']
        
        if orderAsset is None:
            self._orderAsset = OrderAssetDTO()
        else:
            self._orderAsset = orderAsset
    
    def generate_data(self) -> OrderAssetDTO:
        if IDGenerator._last_id is None:
            IDGenerator._last_id = self.__config['first_values']['id']
            
        else:
            random_number = IDGenerator._last_random = PseudoRandom.get_random(IDGenerator._last_random)
            IDGenerator._last_id += random_number

        self._orderAsset.id = IDGenerator._last_id
        return self._orderAsset


class OldDatesGenerator(IGenerator):
    _last_time_increment =  0
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            self._random_amount = 3
            self._step = self.__config['OLD_RECORDS']
            self._first_date = datetime.strptime(self.__config['date']['first_date'], self.__config['date']['config_date_format'])

            
            if OldDatesGenerator._last_random is None:
                OldDatesGenerator._last_random = self.__config['first_values']['old_dates']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset

    def generate_data(self) -> OrderAssetDTO:
        random_numbers = PseudoRandom.get_random_list(OldDatesGenerator._last_random, self._random_amount, self._step)
        OldDatesGenerator._last_random = random_numbers[0]

        time_increment =  (random_numbers[0] % self.__config['date']['max_date_increment']) / 1000
        OldDatesGenerator._last_time_increment = time_increment = time_increment + OldDatesGenerator._last_time_increment

        time_increment = timedelta(seconds=time_increment)
        self._orderAsset.date.append(self._first_date + time_increment)
        
        for j in range(len(random_numbers) - 1):
            time_increment =  (random_numbers[j + 1] % self.__config['date']['max_date_increment']) / 1000
            time_increment = timedelta(seconds=time_increment)
            self._orderAsset.date.append(self._orderAsset.date[-1] + time_increment)
            
        
        if random_numbers[0] % 5 == 0:
            self._orderAsset.date[0] = None

        self._orderAsset.date.insert(0, None)
            
        return self._orderAsset
                

class CurrentDatesGenerator(IGenerator):
    _last_time_increment =  0
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            self._random_amount = 4
            self._step = self.__config['CURRENT_RECORDS']
            self._first_date = datetime.strptime(self.__config['date']['first_date'], self.__config['date']['config_date_format'])

            
            if CurrentDatesGenerator._last_random is None:
                CurrentDatesGenerator._last_random = self.__config['first_values']['current_dates']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset

    def generate_data(self) -> OrderAssetDTO:
        random_numbers = PseudoRandom.get_random_list(CurrentDatesGenerator._last_random, self._random_amount, self._step)
        CurrentDatesGenerator._last_random = random_numbers[0]

        time_increment =  (random_numbers[0] % self.__config['date']['max_date_increment']) / 1000
        CurrentDatesGenerator._last_time_increment = time_increment = time_increment + CurrentDatesGenerator._last_time_increment

        time_increment = timedelta(seconds=time_increment)
        self._orderAsset.date.append(self._first_date + time_increment)
        
        for j in range(len(random_numbers) - 1):
            time_increment =  (random_numbers[j + 1] % self.__config['date']['max_date_increment']) / 1000
            time_increment = timedelta(seconds=time_increment)
            self._orderAsset.date.append(self._orderAsset.date[-1] + time_increment)
            
        return self._orderAsset


class NewDatesGenerator(IGenerator):
    _last_time_increment =  0
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            self._random_amount = 3
            self._step = self.__config['NEW_RECORDS']
            self._first_date = datetime.strptime(self.__config['date']['first_new_date'], self.__config['date']['config_date_format'])

            
            if NewDatesGenerator._last_random is None:
                NewDatesGenerator._last_random = self.__config['first_values']['new_dates']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset

    def generate_data(self) -> OrderAssetDTO:
        random_numbers = PseudoRandom.get_random_list(NewDatesGenerator._last_random, self._random_amount, self._step)
        NewDatesGenerator._last_random = random_numbers[0]

        time_increment =  (random_numbers[0] % self.__config['date']['max_date_increment']) / 1000
        NewDatesGenerator._last_time_increment = time_increment = time_increment + NewDatesGenerator._last_time_increment

        time_increment = timedelta(seconds=time_increment)
        self._orderAsset.date.append(self._first_date + time_increment)
        
        for j in range(len(random_numbers) - 1):
            time_increment =  (random_numbers[j + 1] % self.__config['date']['max_date_increment']) / 1000
            time_increment = timedelta(seconds=time_increment)
            self._orderAsset.date.append(self._orderAsset.date[-1] + time_increment)
            
        
        if random_numbers[-1] % 5 == 0:
            self._orderAsset.date[-1] = None

        self._orderAsset.date.append( None)
            
        return self._orderAsset


class AllDatesGenerator(IGenerator):
    def __init__(self, old_records_amount:int, cur_records_amount:int, new_records_amount:int, orders:Iterable[OrderAssetDTO] = None) -> None:
        self.__config = Config()
        if orders is None:
            self._orderAsset = [OrderAssetDTO() for i in range(old_records_amount + cur_records_amount + new_records_amount)]
        else:
            self._orderAsset = orders
        self.__new_record_amount = new_records_amount
        self.__cur_record_amount = cur_records_amount
        self.__old_record_amount = old_records_amount

    def generate_data(self) -> Iterable[OrderAssetDTO]:
        #getting all dates
        generator = OldDatesGenerator(self.__old_record_amount, self._orderAsset[0:self.__old_record_amount])
        old_dates = generator.generate_data()
        generator = CurrentDatesGenerator(self.__cur_record_amount, self._orderAsset[self.__old_record_amount: self.__old_record_amount + self.__cur_record_amount])
        current_dates = generator.generate_data()
        generator = NewDatesGenerator(self.__new_record_amount, self._orderAsset[self.__old_record_amount + self.__cur_record_amount:])
        new_dates = generator.generate_data()
        
        #formatting some values
        for i in range(len(old_dates)):
            old_dates[i].date.insert(0, None)
        for i in range(len(new_dates)):
            new_dates[i].date.append(None)

        return old_dates + current_dates + new_dates


class StatusGenerator(IGenerator):
    def __init__(self, orderAsset:OrderAssetDTO = None) -> None:
            self.__config = Config()
            
            if StatusGenerator._last_random is None:
                StatusGenerator._last_random = self.__config['first_values']['third_status']
            
            if orderAsset is None:
                self._orderAsset = OrderAssetDTO()
            else:
                self._orderAsset = orderAsset


    def generate_data(self) -> OrderAssetDTO:
        if len(self._orderAsset.status) != 0:
            return self._orderAsset

        random_number = StatusGenerator._last_random = PseudoRandom.get_random(StatusGenerator._last_random)
        self._orderAsset.status = [self.__config['statuses'][0],
            self.__config['statuses'][1],
            self.__config['statuses'][2][random_number % len(self.__config['statuses'][2])],
            self.__config['statuses'][3] ]
        return self._orderAsset
    
