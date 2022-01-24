from FastAPIDemo import oAuth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, Schemas, utils
from ..Database import get_db

#------------------------------Routing Parameter---------------------------

router = APIRouter(
    prefix="/users", tags= ['USERS']
)

#------------------------------Creating User-------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Schemas.UserCreationResponse)
def createUser(userdetails: Schemas.user, db: Session = Depends(get_db)):

    #Hashing Password
    #hashedPassword = pwd_context.hash(userdetails.password)
    #userdetails.password = hashedPassword
    userdetails.password = utils.hash(userdetails.password)
    newUser = models.User(**userdetails.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    print(userdetails.dict())
    return newUser

@router.get("/{user_id}", response_model=Schemas.UserCreationResponse)
def getUser(user_id: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {user_id} does not exist")
    
    return result