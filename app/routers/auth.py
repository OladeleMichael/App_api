from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..import database, schemas, models, utils, oauth2

router = APIRouter(tags=['authentication'])

@router.post ('/login',response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): #store user login in a variable user_credentials

#find user email in db
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #query the db for user email and stores in variable user

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid Credentials")

#compare inserted hash password with database password
    if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid Credentials")


#create token
#return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type":"bearer"}