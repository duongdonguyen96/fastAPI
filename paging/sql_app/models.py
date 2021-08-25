import re
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime, Time
from pydantic import BaseModel, ValidationError, validator
from .database import Base
from pydantic import BaseModel, Field


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    
    def validation_email( email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
        if(re.fullmatch(regex, email)):
            return "Invalid Email"
        return email    

    
    def validation_password( password):
        if ' ' in password:
            raise ValueError('contain a space')
        return password




class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    comments = relationship("Comment", back_populates="item")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    writer_id = Column(String, index=True)
    content = Column(String, index=True)
    time_comment = Column(DateTime, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))

    item = relationship("Item", back_populates="comments")






