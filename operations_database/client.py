##pip install mysql-connector-python
##pip install mysqlclient 
##pip install mariadb
##pip install sqlalchemy
##pip install python-dotenv

import datetime

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


from DataBase import DataBase as db

class Base(DeclarativeBase):
     pass

class ClientCreated(Base):
        __tablename__="client"
    
        ID_CLIENT: Mapped[int] = mapped_column(primary_key=True)
        CLIENT_ID_FACEBOOK: Mapped[int] = mapped_column(Integer)
        CLIENT_SECRET_FACEBOOK: Mapped[int] = mapped_column(Integer)
        PAGE_ID_FACEBOOK: Mapped[int] = mapped_column(Integer)
        ACCESS_TOKEN: Mapped[str] = mapped_column(String)
        READ_AT: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True), 
            server_default=func.now()
        )
        INSERT_AT: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True), 
            server_default=func.now()
        )
        UPDATE_AT: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True), 
            server_default=func.now()
        )
        DELETED_AT: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True), 
            server_default=func.now()
        )

        def __repr__(self):
               return f"Post (id cliente={self.ID_CLIENT}, {self.READ_AT}, {self.UPDATE_AT}, {self.DELETED_AT})"
        
    

class Client(db):
    def __init__(self):
        super().__init__()
       
    def ClientRecorded(self):
        return self.query(ClientCreated,'', 'INSERT_AT ASC')
    

if __name__=='__main__':
    print('teste')

    client = Client()

    session = Session(client.engine)
    stmt = client.ClientRecorded()
    for client1 in session.scalars((stmt)):
        print(client1)