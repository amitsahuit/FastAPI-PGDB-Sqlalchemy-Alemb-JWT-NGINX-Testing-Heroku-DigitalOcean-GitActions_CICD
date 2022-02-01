from fastapi.testclient import TestClient
from FastAPIDemo.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print("res.status_code value is :", res.status_code)
    assert res.status_code == 200
    print("res.json() value is :",res.json())
    assert res.json() == {"message": "Hello World lets try Digital Ocean & Heroku with Docker...!!!!!!! hurray"}

from FastAPIDemo import Schemas
def test_create_user():
    res = client.post("/users/", json={"username": "amit_5", "email": "amit_5@gmail.com", "password": "amit"})
    print("res.json value is :",res.json)
    print("res.json().get(\"email\") value is: ", res.json().get("email"))
    assert res.json().get("email") == "amit_5@gmail.com"
    assert res.status_code  == 201
    
    # Lets check if the created user has all the values which UserCreationResponse has.
    new_user = Schemas.UserCreationResponse(**res.json()) #doing a pydantic validation
    print(Schemas.UserCreationResponse(**res.json()))
    assert new_user.email == "amit_5@gmail.com"

    