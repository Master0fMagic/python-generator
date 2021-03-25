import logging
from typing import Any
import os
import sys
from my_config import Config

class Logger:
    __loger = None

    def __new__(cls) -> Any:
        try:
            if cls.__loger is None:
                cls.__loger = logging.getLogger()
                cls.__setup_logger(cls)
            return cls.__loger
        except Exception as ex:
            print(f'Error while setuping logger: {ex}')
            sys.exit(1)
    
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
            print(f'Error while setuping logger: {ex}')
            sys.exit(1)