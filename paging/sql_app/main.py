
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas,token, oauth2

from .database import SessionLocal, engine
from .hash import Hash
from typing import List

models.Base.metadata.create_all(bind=engine)

from fastapi import FastAPI, Depends
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Authen

@app.post('/login',tags=['Authentication'])
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/api/me", response_model=schemas.User)   
# async def get_current_active_user(current_user: schemas.User = Depends(oauth2.get_current_user)):
#     return current_user


# User
@app.post("/users/", response_model=schemas.User, tags=['user'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    models.User.validation_email(user.email)
    models.User.validation_password(user.password)

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@app.patch("/users/{user_id}",tags=['user'])
def update_user(user_id: int,user: schemas.UserUpdate, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    result = crud.get_user(db,user_id)
    if result is None:
        return "User is not exist"
        
    respon_user = crud.update_user(db, user_id, user=user)
    return respon_user


@app.delete("/users/{user_id}",tags=['user'])
def delete_user(user_id: int  , db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User is not exits")
    status = crud.delete_user(db=db, user_id=user_id)
    return status  


@app.get("/users/search/", response_model=List[schemas.User],tags=['user'])
def read_user(email:str , db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_user = crud.search_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=List[schemas.User],tags=['user'])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@app.get("/users/{user_id}", response_model=schemas.User,tags=['user'])
def read_user(user_id: int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


#item

@app.post("/users/{user_id}/items/", response_model=schemas.Item,tags=['post'])
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item],tags=['post'])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.delete("/item/{item_id}",tags=['post'])
def delete_item(item_id: int  , db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_item = crud.get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=400, detail="item is not exits")
    status = crud.delete_item(db=db, item_id=item_id)
    return status  

# Comment

@app.post("/item/{item_id}/comment/", response_model=schemas.Comment,tags=['comment'])
def create_comment(item_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_item = crud.get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=400, detail="item is not exits")
   
    return crud.create_comment(db=db,comment=comment, item_id=item_id)


@app.get("/comments/", response_model=List[schemas.Comment],tags=['comment'])
def read_comment(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    items = crud.get_comments(db, skip=skip, limit=limit)
    return items   


@app.patch("/comments/{comment_id}",tags=['comment'])
def update_comment(commen_id: int,comment: schemas.CommentUpdate, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_comment = crud.get_comment(db,commen_id)
    if db_comment is None:
        return "commenit s not exist"
        
    respon_comment = crud.update_comment(db, commen_id, comment,db_comment)
    return respon_comment


@app.delete("/comments/{comment_id}",tags=['comment'])
def delete_comment(comment_id: int  , db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_comment = crud.get_comment(db,comment_id)
    if not db_comment:
        raise HTTPException(status_code=400, detail="commenit is not exits")
    status = crud.delete_comment(db=db,comment_id=comment_id)
    return status  




