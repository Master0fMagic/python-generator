from typing import Any
import config as cfg
import sys

class Config:
    __config_file = 'config.cfg'
    __config_data = None

    def __new__(cls) -> Any:
        try:
            if cls.__config_data is None:
                cls.__config_data = cfg.Config(cls.__config_file)
            return cls.__config_data
        except Exception as ex:
            print(f'Error while setting config: {ex}')
            sys.exit(1)
