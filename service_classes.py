from typing import Any
import config
import logging
import os
import sys

class DBService:
    pass

class Config:
    __config_file = 'config.cfg'
    __config_data = None

    def __new__(cls) -> Any:
        try:
            if cls.__config_data is None:
                cls.__config_data = config.Config(cls.__config_file)
            return cls.__config_data
        except Exception as ex:
            raise ex

class Logger:
    __loger = None

    def __new__(cls) -> Any:
        try:
            if cls.__loger is None:
                cls.__loger = logging.getLogger()
                cls.__setup_logger(cls)
            return cls.__loger
        except Exception as ex:
            raise ex
    
    @staticmethod
    def __setup_logger(cls) -> None:
        config = Config()
        try:
            if not os.path.exists(config['logging']['log_path']):
                dir_path = os.path.dirname(config['logging']['log_path'])
                os.mkdir(dir_path)
            
            handler = logging.FileHandler(filename=config['logging']['log_path'], mode='a')
            handler.setLevel(logging.getLevelName(config['logging']['level']))
            formatter = logging.Formatter(config['logging']['format'])
            
            cls.__loger.setLevel(logging.getLevelName(config['logging']['level']))
            handler.setFormatter(formatter)
            cls.__loger.addHandler(handler)
        except Exception as ex:
            raise ex

class PseudoRandom:
    __A=1366
    __C=150889
    __M=714025

    @staticmethod
    def get_M() -> int:
        return PseudoRandom.__M

    @staticmethod
    def get_C() -> int:
        return PseudoRandom.__C

    @staticmethod
    def get_A() -> int:
        return PseudoRandom.__A

    @staticmethod
    def get_random(number:int):
        return (PseudoRandom.__A*number + PseudoRandom.__C) % PseudoRandom.__M

    @staticmethod 
    def get_random_list(first_value:int, row_amount:int, sets_amount:int = 1):
            blank_sheet = [[] for i in range(sets_amount)]
            pr_number = None
            for i in range(len(blank_sheet)):
                if i == 0:
                    pr_number = PseudoRandom.get_random(first_value)
                else:
                    pr_number = PseudoRandom.get_random(blank_sheet[i-1][-1])
                blank_sheet[i].append(pr_number)

                for j in range(1,row_amount):
                    pr_number = PseudoRandom.get_random(blank_sheet[i][j-1])
                    blank_sheet[i].append(pr_number)
            if len(blank_sheet) == 1:
                return blank_sheet[0] 
            return blank_sheet

