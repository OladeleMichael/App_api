from fastapi import FastAPI, Response, Request, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags= ['Users']
)


@router.post("/" ,status_code=status.HTTP_201_CREATED , response_model=schemas.UserOut)
def create_user ( user: schemas.UserCreate, db: Session = Depends(get_db)):

    #user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    
    #if user_exist:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        #                     detail= f"User with email: {user.email} already exists!")
  
    #if user:

    try:
        hashed_password = utils.hash(user.password) #hash the password - user.password 
        user.password = hashed_password #store hashed the password in user.password
        
        new_user = models.User( **user.dict()) # another way to do this is (title= post.title, content= post.content, published = post.published)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return  new_user # this is the response  returned to the client on success.

    except:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail= f"User with email: {user.email} already exists!")
        

@router.get ("/{id}", response_model=schemas.UserOut )
def get_user (id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter (models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"User with id: {id} does not exist!")
        #response.status_code= status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id: {id} was not found"}
    return user