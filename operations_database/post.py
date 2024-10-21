# -*- coding: utf-8 -*-
##pip install mysql-connector-python
##pip install mysqlclient 
##pip install mariadb
##pip install sqlalchemy
##pip install python-dotenv


import os 
import sys
from dotenv import load_dotenv


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)


import datetime
from sqlalchemy import text
from sqlalchemy import BLOB, String, DateTime, Integer, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
#from IPython.display import display

from PIL import Image
from io import BytesIO

#from sqlalchemy.dialects.mysql import mysql


from operations_database.DataBase import DataBase as db


class Base(DeclarativeBase):
     pass

class PostCreated(Base):
        __tablename__="post"
    
        ID_POST: Mapped[int] = mapped_column(primary_key=True)
        ID_CLIENT: Mapped[int] = mapped_column(Integer)
        TITLE: Mapped[str] = mapped_column(String(200))
        LOCATION: Mapped[str] = mapped_column(String(100))
        MODALITY: Mapped[str] = mapped_column(String(20))
        MESSAGE: Mapped[str] = mapped_column(String(2200))
        IMAGE_MESSAGE: Mapped[str] = mapped_column(String(2200))
        LINK: Mapped[str] = mapped_column(String(200))
        IMAGE_POST_NAME: Mapped[str] = mapped_column(String(30))
        #IMAGE_POST:Mapped[BLOB] = mapped_column(BLOB)
        INSERT_AT: Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True), 
            server_default=func.now()
        )
        def __repr__(self):
               return f"Post (id_post={self.ID_POST}, id_cliente={self.ID_CLIENT}, {self.TITLE}, {self.LOCATION}, {self.MODALITY}, {self.MESSAGE}, {self.IMAGE_MESSAGE}, {self.LINK}, {self.IMAGE_POST_NAME}, {self.INSERT_AT})"
        
    
class Post(db):
    def __init__(self):
        super().__init__()
       
    def PostRevised(self):
        return self.query(PostCreated,' POSTED_AT IS NULL AND REVISED_AT IS NOT NULL ', 'INSERT_AT ASC')
    
        

if __name__=='__main__':
    print('teste')

    post = Post()
    session = Session(post.engine)
    stmt = post.PostRevised()
    for post1 in session.scalars((stmt)):
        print(post1)

    #exit(0)
    load_dotenv()
    path = os.getenv("PATH_ROOT")

    image_name = 'image0.png'

    img_pil = Image.open(image_name, path)
    #img_rec= open(path+'\\'+image_name,'rb').read()
    #fullPathImage = path+"\\"+image_name
    ##fullPathImage = '\post_created\image0.png'
    

    with open(fullPathImage, 'x') as f:
        img_data = f.read()
        session.add(img_data)
        session.commit()
        session.close()
        print(" Fim ")


    ##UpdatePostWithImage()

    #img_pil.show()
    ##print(img_rec)
    ##exit(0)







