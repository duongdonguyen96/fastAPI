from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import DateTime

# Class Comment
class CommentBase(BaseModel):
    content: str

class Comment(CommentBase):
    id:int
    item_id:int
    writer_id:int
    
    class Config:
        orm_mode = True

class CommentCreate(CommentBase):
    pass 

class CommentUpdate(CommentBase):
    pass   

# Class Item
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True  

# Class User
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []
    hashed_password:str

    class Config:
        orm_mode = True

#Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None



   
