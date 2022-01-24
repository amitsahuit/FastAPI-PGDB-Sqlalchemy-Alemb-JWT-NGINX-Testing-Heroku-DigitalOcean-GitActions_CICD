from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import models, Schemas, Database

# to get a string like this run --> openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30 #This value is in minute.

from .config import setting
SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()

    """Remember the expire time will always be utcnow() not now()"""
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    """Encoding the payload"""
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #--> (Payload, secret key, Algorith)
    return encoded_jwt




"""this function will take the token (hashed) as a function parameter then decode it and return the output in TokenData schema format"""
def verify_access_token(token: str, credentials_exception ):
    try:
        """decoding the payload"""
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        """getting the "user_id" which we passed in Auth.py file
        access_token = oAuth2.create_access_token(data={"user_id":result.id})"""
        id: str = payload.get("user_id")

        """Verifying the token"""
        if id is None:
            raise credentials_exception

        """we have created a response schema "TokenData" to hold the output data"""
        token_data = Schemas.TokenData(userID=id)
    except JWTError:
        raise credentials_exception

    return token_data




"""We can pass this get_current_user function to any path operation as "Depends" and it will do the below things;
1. take the token form the request body automatically --> by returning verify_access_token function
2. Extract the ID/data for us --> by returning verify_access_token function
3. Verify the token is correct or not --> by returning verify_access_token function
4. and its going to extract an ID --> by returning verify_access_token function
5. and if we want to we can automaticlaly fetch the ID from DB and add as a parameter into our path operations functions"""

from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

#this is going to be our login endpoint present in auth.py "@router.post('/login')"
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login") 

# we can pass the above oauth2_schema into this method
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(Database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    Usertoken = verify_access_token(token, credentials_exception)    

    #Trying to return complete user details not only ID.
    user = db.query(models.User).filter(models.User.id == Usertoken.userID).first()
    print("User Name is: ",user.username)
    return user

