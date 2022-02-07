from pydantic import BaseModel
from typing import Optional
from datetime import datetime

""" it will hold the respose in Auth.py file --> @router.post('/login', response_model=Schemas.Token)"""
class Token(BaseModel):
    access_token: str
    token_type: str


"""It will use to hold the data from verify_access_token method"""
class TokenData(BaseModel):
    userID: Optional[str] = None


class Item(BaseModel):
    first_name: str
    last_name:str
    id: Optional[float] = None
    age: int
    addresss: Optional[str] =None
    passport: Optional[bool] = False


from pydantic import EmailStr
class user(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreationResponse(BaseModel):
    #Because we dont want to show password we extended BaseModel instead of user schema
    email: EmailStr
    id: int
    createdtime: datetime
    class Config:
        orm_mode = True


class partnerArrayModel(BaseModel):
    partnername: str
    partnerfunction: str
    rating: int = 4


class createPartner(partnerArrayModel):
    pass


class PartnerResponseSchema(partnerArrayModel):
    id: int
    createdtime: datetime
    # Will grab the user_id from the logged in token and return it in schema
    owner_id: int
    #returning a Pydantic model of User Response
    owner: UserCreationResponse
    class Config:
        orm_mode = True


from pydantic.types import conint
class Vote(BaseModel):
    partner_id: int
    direction: conint(le=1)