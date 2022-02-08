from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
#from . import models
#from .Database import engine, get_db
from .routers import ItemsCRUD, PartnerCRUD, UserCRUD, Auth, FileOperation, VotesCRUD
from .config import Settings    

"""-----------------------------DB Operations with SQLALCHEMY----------------------------------"""

"""This command will tell SQL Alchemy to run the create statement to generate all teh tables when it start.
    Since we have alembic so we no longer need this command
    Keeping this command will not break anything."""
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""Setting up middleware for CORS policy"""
from fastapi.middleware.cors import CORSMiddleware

origins = [
    #"https://www.google.co.in",
    #"https://www.google.com",
    #"*" #This is a wild card means all the websites can make request to my api.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(Auth.router)
app.include_router(UserCRUD.router)
app.include_router(UserCRUD.router)
app.include_router(PartnerCRUD.router)
app.include_router(VotesCRUD.router)
app.include_router(ItemsCRUD.router)
app.include_router(FileOperation.router)

#-----------------------------------------------Testing purpose-----------------------------------------------
@app.get("/")
async def root():
    return {"message": "trying CICD in heroky"}

# @app.get("/SQlAlchemyDemo")
# async def SQlAlchemyDemo(db: Session = Depends(get_db)):
#     partner_list=db.query(models.Partners).all()
#     return partner_list



