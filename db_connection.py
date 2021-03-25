from typing import Any
import sys
import mysql.connector
from mysql.connector import errorcode
from logger import Logger

class DBService:
    __connection = None
    
    def __new__(cls) -> Any:
        if cls.__connection is None:
            try:
                cls.__connection = mysql.connector.connect(user='root', password='root',
                                    host='127.0.0.1',
                                    database='generator')
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print(f"Something is wrong with your user name or password: {err}")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print(f"Database does not exist: {err}")
                else:
                    print(f"Error while connecting to database: {err}")
                sys.exit(1)
        return cls.__connection
    
    def __init__(self) -> None:
        self.__loger = Logger()
        self.__loger.info("Connected to database")


    def __del__(self):
        try:
            self.__connection.close()
            self.__connection = None
        except Exception as e:
            print('Exception while closing database connection: {ex}')
            self.__loger.error('Exception while closing database connection: {ex}')
            sys.exit(1)