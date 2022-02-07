from sys import modules
from FastAPIDemo.config import setting
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from FastAPIDemo.Database import get_db
from FastAPIDemo.Database import Base
import pytest
from fastapi.testclient import TestClient
from FastAPIDemo.main import app
"""-----------------------------DB Operations with SQL Alchemy starts----------------------------------"""

#SQLALCHEMY_DATABASE_URL = "postgresql://<userName>:<password>@<IP address>/<db name>"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sys@localhost:5432/fastapidb1_test"
SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.DATABASE_USERNAME}:{setting.DATABASE_PASSWORD}@{setting.DATABASE_HOSTNAME}:{setting.DATABASE_PORT}/{setting.DATABASE_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()
# from FastAPIDemo.Database import Base
# Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def session():
    print("Droping all tables")
    Base.metadata.drop_all(bind=engine) # It will drop all the tables
    print("Creating all tables")
    Base.metadata.create_all(bind=engine) # IT will recreate all the tables
    db = TestingSessionLocal()
    try:
        print("Opening the DB session from TestingSessionLocal")
        yield db
    finally:
        db.close()

"""-----------------------------DB Operations with SQL Alchemy ends----------------------------------"""


#client = TestClient(app)
# Adding fixtures
#@pytest.fixture(scope="module")
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            print("Yielding the session which was passed into client")
            yield session
        finally:
            session.close()
    
    # this below command will swap the get_db with override_get_db method 
    # when its being called from any method's "db: Session = Depends(get_db)""
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) # yield is same as return but it gives flexiblity to run code after returnng.
    