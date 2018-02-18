import os
import sys #provides functions and variables that can be used to manipulate different parts of python run time env.
from sqlalchemy import Column, ForeignKey, Integer, String #useful when writing mapper code
from sqlalchemy.ext.declarative import declarative_base #will be used in the configuration and class code
from sqlalchemy.orm import relationship #to create foreign key relationships and useful in mapper
from sqlalchemy import create_engine #used in configuration code

Base = declarative_base() #will let sqlalchemy know that our classes are special sqlalchemy classes that correspond to tables in db.
class Restraunt(Base):#table in db
    __tablename__ = 'restraunt'#table name in db
    name = Column(String(80),nullable = False)
    id = Column(Integer,primary_key = True)


class MenuItem(Base):#table in db
    __tablename__ = 'menu_item'#table name in db
    name = Column(String(80),nullable = False)
    id = Column(Integer,primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restraunt_id = Column(Integer,ForeignKey('restraunt.id'))
    restraunt = relationship(Restraunt)
engine = create_engine('sqlite:///restrauntmenu.db') # create_engine instance that points to our database.
Base.metadata.create_all(engine) # goes into the db and adds the classes as new tables in our database
