from FastAPIDemo import models
from FastAPIDemo.oAuth2 import create_access_token
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

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()
# from FastAPIDemo.Database import Base
# Base.metadata.create_all(bind=engine)

#@pytest.fixture(scope="module")


@pytest.fixture()
def session():
    print("Droping all tables")
    Base.metadata.drop_all(bind=engine)  # It will drop all the tables
    print("Creating all tables")
    Base.metadata.create_all(bind=engine)  # IT will recreate all the tables
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
    # yield is same as return but it gives flexiblity to run code after returnng.
    yield TestClient(app)

# this test user is for testing the login functionality.


@pytest.fixture()
def test_user(client):
    user_data = {"username": "test",
                 "email": "test@gmail.com", "password": "test"}
    res = client.post("/users/", json=user_data)
    print("test_user JSON value is :", res.json())
    assert res.status_code == 201

    # Note: if the user created succesfully then in response we wont get the password. So we need to create a new variable and
    # add the newly provided password field in that new variable.
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    # --> Refer Auth.py --> login --> access_token there we had passes "user_id"
    return create_access_token({"user_id": test_user['id']})

#The client we had created above is not authorized So lets create a authorised client


@pytest.fixture
def authorized_client(client, token):
    #We need to pass the token inside the headers of unauthorized client and return that updated authorized client
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_user2(client):
    user_data = {"username": "test2",
                 "email": "test2@gmail.com", "password": "test2"}
    res = client.post("/users/", json=user_data)
    print("test_user JSON value is :", res.json())
    assert res.status_code == 201

    # Note: if the user created succesfully then in response we wont get the password. So we need to create a new variable and
    # add the newly provided password field in that new variable.
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_partner(session, test_user, test_user2):
    partner_data = [{"partnername": "first test partner", "partnerfunction": "Seller", "rating": 4, "owner_id": test_user['id']},
                    {"partnername": "second test partner", "partnerfunction": "retailler",
                        "rating": 4, "owner_id": test_user['id']},
                    {"partnername": "third test partner", "partnerfunction": "warehouse",
                        "rating": 4, "owner_id": test_user['id']},
                    {"partnername": "fourth test partner", "partnerfunction": "ttransportation",
                        "rating": 4, "owner_id": test_user2['id']}]

    def create_partner_model(partner_value):
        return models.Partners(**partner_value)

    # using the above partner_data dict and adding into partners table.
    # this map function will take the values from teh partner_data dict and convert that into "models.partners"
    partner_map = map(create_partner_model, partner_data)
    # the above will return a map so we need to convert it into list
    partners = list(partner_map)
    session.add_all(partners)

    # Manually adding the values not using the above cretaed partner_data dict
    # session.add_all([models.Partners(partnername="first test partner", partnerfunction="Seller", rating=4, owner_id=test_user['id']),
    #                 models.Partners(title="Second test partner", content="Seller", rating=4, owner_id=test_user['id']),
    #                 models.Partners(title="Third test partner", content="Seller", rating=4, owner_id=test_user['id'])
    #                 ])
    session.commit()

    partners_select_all = session.query(models.Partners).all()
    return partners_select_all
