from config import SQLLITE_DB_PATH
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData


class SingletonDataBaseConnectivitySQLIte(object):
    
    engine = None
    connection_instance = None
    connection = None
    instance = None
    instance_state = False
    base = None
    
    def __new__(cls, drivername:str = 'sqlite://', path:str = SQLLITE_DB_PATH):
        
        cls.drivername = f"{drivername}/{path}"
        if cls.engine is None or cls.connection_instance:
            print("connecting....")
            cls.engine = create_engine(cls.drivername)
            cls.connection = cls.engine.connect()
            cls.connection_instance = cls.connection.closed
            print("connection completed!")
            cls.instance = cls
            cls.base = declarative_base()
        return cls.instance
    
    @classmethod
    def get_engine(cls):
        print("checking for engine activity")
        if not cls.connection.closed:
            print("engine connection is live!")
            cls.connection_instance = False
            return cls.engine
        cls()
        return cls.engine
    
    @classmethod
    def get_session(cls):
        engine = cls.get_engine()
        return Session(bind = engine)
    
    @classmethod
    def close_the_connection(cls):
        cls.connection.close()
        cls.connection_instance = True


# db = SingletonDataBaseConnectivitySQLIte()