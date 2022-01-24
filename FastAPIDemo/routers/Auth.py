from FastAPIDemo import utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, Schemas, oAuth2
from ..Database import get_db

router=APIRouter(
    tags=['AUTHENTICATION']
)

"""This method will create a token and give it to user which they can use to access API path operation via postman"""
@router.post('/login', response_model=Schemas.Token)
#def login(inputVal: Schemas.UserLogin, db: Session = Depends(get_db)):
def login(inputVal: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2PasswordRequestForm will return only 2 values (username, password) 
    no matter what u give (id, email, username) it will treat it as username and the password will be treated as password."""

    result = db.query(models.User).filter(models.User.email == inputVal.username).first()
    if not result:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail=f"user with emil ID {inputVal.username} is not present")
    
    if not utils.verification(inputVal.password, result.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    access_token = oAuth2.create_access_token(data={"user_id":result.id})
    return {"access_token":access_token, "token_type": "bearer"}
