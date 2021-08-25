from os import write
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import true
from datetime import datetime

from sqlalchemy.sql.functions import mode
from . import models, schemas
from .hash import Hash
from random import randint

# //User Service

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def search_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email.contains(email)).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# Delete User and list item

def delete_user(db: Session,user_id: int):
    # delete list item
    db.query(models.Item).filter(models.Item.owner_id == user_id).delete()

    # delete user
    db_user=db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return "Delete User and Delete list item Success"  



def create_user(db: Session, user: schemas.UserCreate):
    password=Hash.bcrypt(user.password)

    db_user = models.User(email=user.email, hashed_password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    password = Hash.bcrypt(user.password)
    #query nhieu
    current_user =  get_user (db,user_id)
    current_user.email = user.email
    current_user.hashed_password = password
 
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    response_object = {
        "id": user_id,
        "email": user.email,
        "password": password,
    }
    return response_object     


# // Iteam Service
def get_item(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):

    db_comment = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_item(db: Session,item_id: int):
    # delete list comment
    db.query(models.Comment).filter(models.Comment.item_id == item_id).delete()

    # delete item
    db_user=db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_user)
    db.commit()
    return "Delete Post and Delete list Comment Success"      

# Comment
def get_comment(db: Session, comment_id: int):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    return comment

def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()

def create_comment( db: Session, comment: schemas.CommentCreate, item_id: int):
    # user = self.user
    time_now = datetime.now()
    writer_id = randint(0, 1000)

    db_comment = models.Comment(item_id=item_id, content=comment.content,time_comment=time_now,writer_id=writer_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session,comment_id: int):
    db_comment=db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    db.delete(db_comment)
    db.commit()
    return "Delete comment Success"


def update_comment(db: Session, comment_id: int, comment_rq: schemas.CommentUpdate , db_comment : models.Comment):

    db_comment.content = comment_rq.content  
 
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    response_object = {
        "id": db_comment.id,
        "item_id": db_comment.item_id,
        "content": db_comment.content,
        "writer_id": db_comment.writer_id,
        "time_comment": db_comment.time_comment
    }
    return response_object               

