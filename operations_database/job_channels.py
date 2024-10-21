##pip install mysql-connector-python
##pip install mysqlclient 
##pip install mariadb
##pip install sqlalchemy
##pip install python-dotenv

import datetime

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from DataBase import DataBase as db

class Base(DeclarativeBase):
     pass

class jobChannels(Base):
        __tablename__="job_channels"
    
        ID_JOB_CHANNELS: Mapped[int] = mapped_column(primary_key=True)
        NAME: Mapped[str] = mapped_column(String(30))
        CHANNEL: Mapped[str] = mapped_column(String(100))
        STATUS: Mapped[int] = mapped_column(Integer)

        def __repr__(self):
               return f"Post (id Channels={self.ID_JOB_CHANNELS}, {self.NAME}, {self.CHANNEL}, {self.STATUS})"
        
    

class job_channels(db):
    def __init__(self):
        super().__init__()
       
    def jobChannelsRecord(self):
        return self.query(jobChannels,'', 'NAME ASC')
    

if __name__=='__main__':
    print('teste')

    job_channel = job_channels()

    session = Session(job_channel.engine)
    stmt = job_channel.jobChannelsRecord()
    for post1 in session.scalars((stmt)):
        print(post1)