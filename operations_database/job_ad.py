##pip install mysql-connector-python
##pip install mysqlclient 
##pip install mariadb
##pip install sqlalchemy
##pip install python-dotenv

from typing import List
from typing import Optional
from sqlalchemy import create_engine, Text, insert, update, delete, select, table, and_, Column, String, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session

import os
from dotenv import load_dotenv

#from DataBase import DataBase as db
from .DataBase import DataBase as db

#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker


load_dotenv()
USERNAME_DB = os.getenv("USERNAMEDB")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DATA_BASE = os.getenv("DATA_BASE")

class Base(DeclarativeBase):
     pass

class JobAd(Base):
        __tablename__= "job_ad"

        ID_JOB_AD: Mapped[int] = mapped_column(primary_key=True)
        TITLE: Mapped[str] = mapped_column(String(200))
        LOCATION:Mapped[str]=mapped_column(String(100))
        MESSAGE: Mapped[str] = mapped_column(String(2200))
        LINK: Mapped[str] = mapped_column(String, nullable=False)
        LOG_SCRAPER:Mapped[str]=mapped_column(Text)
        ID_PAI:Mapped[str]=mapped_column(Integer)

        def __repr__(self):
            return f"job_ad (title={self.TITLE}, {self.MESSAGE}, {self.LINK}), {self.LOG_SCRAPER}), {self.ID_PAI})"
        

"""
Class that writes collected jobs.
"""
class job_ad(db):
    """
    Construct of job_ad class.
    """
    def __init__(self):
        super().__init__()
    

if __name__=='__main__':       
    
    job = job_ad()
    session = Session(job.engine)
    stmt = (job.query(JobAd, 'ID_JOB_AD = 2', 'INSERT_AT DESC'))
    for job1 in session.scalars((stmt)):
        print(job1)

    exit(0)
    

    parans = dict(TITLE="teste123",MESSAGE="teste123",LINK="teste123")
    ##job.insertScript(JobAd, parans)

    ##job.deleteScript(JobAd, 'ID_JOB_AD=73')

    """
    query = " SELECT * FROM job_ad "
    res = job.queryRaw( (query) )

    for row in res:
        print(row)
    """
    ##query2 = text(""" INSERT INTO regime(description) VALUES(:description) """)
    ##data = []
    ##data['description'] = "SextS"


    #job.connection.execute(query2, data)

    ##job.insert(query2, data)
    """
    job = job_ad()
    session = Session(job.engine)
    stmt = select(JobAd).where(JobAd.ID_JOB_AD == 1)
    
    for job1 in session.scalars(stmt):
        print(job1)
    """

    