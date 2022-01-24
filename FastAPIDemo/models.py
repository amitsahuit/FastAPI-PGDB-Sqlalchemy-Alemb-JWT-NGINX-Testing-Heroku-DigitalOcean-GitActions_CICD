from sqlalchemy.sql.schema import ForeignKey
from .Database import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Partners(Base):
    __tablename__='partner'
    id=Column(Integer, nullable=False, primary_key=True)
    partnername=Column(String, nullable=False)
    partnerfunction=Column(String, nullable=False, server_default="Supplier")
    rating=Column(Integer,nullable=False)
    published=Column(Boolean, nullable=False, server_default='True')
    createdtime=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    #Creating foreign key by using "users.id" as primary key 
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)    

    #Setting up a relationship
    from sqlalchemy.orm import relationship
    # The input to relaionship() is the class name "User" not the tablename "users"
    owner = relationship("User") 

class User(Base):
    __tablename__='users'
    id=Column(Integer, nullable=False, primary_key=True)
    username=Column(String, nullable=False)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    createdtime=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    Phone_number=Column(Integer)

# We are making composit key in Votes class by making both columns as primary key.
class Vote(Base):
    __tablename__='votes'
    partner_id=Column(Integer, ForeignKey("partner.id", ondelete="CASCADE"), primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    