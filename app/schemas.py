from pydantic import BaseModel, validator, ValidationError, validate_email,EmailStr
from datetime import datetime
from typing import Any, Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True
    #rating: Optional [int] = None 
    # @validator('title', pre=True, always=True)
    # def set_ts_now(cls, v):
    #     return v or datetime.now()

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    firstname: str
    lastname: str
    id: int
    email: EmailStr
    created_at: datetime 
    
    class Config:
       orm_mode = True 

class PostUpdate(PostBase):
    pass

# this class is used in manipulating the data that a user recieves in the REST call response(can inherit other parameters from PostBase class), in short what the user see.
class Post(PostBase):
    owner_id: int
    id: int
    created_at: datetime 
    owner: UserOut
    
    class Config:
       orm_mode = True 

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
       orm_mode = True 

class UserCreate (BaseModel):
    firstname:str
    lastname:str
    email: EmailStr
    password: str
    phone_number:str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None 

#voting or likes

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
       orm_mode = True 
