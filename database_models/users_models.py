from utilities.data_base_connectivity_utils import SingletonDataBaseConnectivitySQLIte
from sqlalchemy import Column, String

class Users(SingletonDataBaseConnectivitySQLIte().base):

    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    password = Column(String)
    
