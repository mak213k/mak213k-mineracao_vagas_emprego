##pip install mysql-connector-python
##pip install mysqlclient 
##pip install mariadb
##pip install sqlalchemy
##pip install python-dotenv

from typing import List
from typing import Optional
from sqlalchemy import create_engine, text, insert, update, delete, select
from sqlalchemy import table, and_, Column, String, MetaData, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session

import os
from dotenv import load_dotenv



#from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
USERNAME_DB = os.getenv("USERNAMEDB")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATA_BASE = os.getenv("DATA_BASE")


"""
Class that writes collected jobs.
"""
class DataBase:
    """
    Construct of job_ad class.
    """
    def __init__(self):
        host_connection = 'mysql+pymysql://'+str(USERNAME_DB)+':'+str(PASSWORD)+'@'+str(HOST)+':'+str(PORT)+'/'+str(DATA_BASE) +'?charset=utf8'
        self.engine = create_engine(host_connection)
        self.connection = self.engine.connect()

    """
    Function that query raw sql scripts.
    """
    def queryRaw(self, query):
        results = self.connection.execute(text(query))
        return results.fetchall()
    
    """
    Function that insert raw sql.
    """
    def insertRaw(self, query, data):
        self.connection.execute(text(query), **data)
        self.connection.commit()
        return

    """
    Function that sql alchemy run ORM.
    """
    def query(self, table, where, orderBy, join=''):
        stmt = select(table).where(text(where)).order_by(text(orderBy))
        return stmt
        
    """
    Function that sql insert alchemy run ORM.
    """
    def insertScript( self, table, coluns=[] ):
        stmt = insert(table).values(coluns)
        self.connection.execute(stmt)
        self.connection.commit()
        return 
    
    """
    Function that sql update alchemy run ORM.
    """
    def updateScript( self, table, coluns, where ):
        
        stmt = update( table ).where( text(where) ).values(coluns)
        
        self.connection.execute(stmt)
        self.connection.commit()
        return
    
    """
    Function that sql delete alchemy run ORM.
    """
    def deleteScript( self, table, where_condition):
        stmt = delete(table).where( text(where_condition) )
        self.connection.execute(stmt)
        self.connection.commit()
        return

if __name__=='__main__':
    print(os.getenv("HOST"))
    exit(0)
    print('teste')
    ja = job_ad()
    dd = DataBase()
    session = Session(ja.engine)
    stmt = dd.query(ja, 'ID_JOB_AD = 2', 'INSERT_AT DESC')

    for job1 in session.scalars(stmt):
        print(job1)