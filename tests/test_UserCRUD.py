import pytest
from FastAPIDemo import Schemas, models
#from .Database import *

# def test_root(client):
#     res = client.get("/")
#     print("res.status_code value is :", res.status_code)
#     assert res.status_code == 200
#     print("res.json() value is :", res.json())
#     assert res.json() == {
#         "message": "Hello World lets try Digital Ocean & Heroku with Docker...!!!!!!! hurray"}


def test_create_user(client):
    res = client.post(
        "/users/", json={"username": "amit_5", "email": "amit_5@gmail.com", "password": "amit"})
    print("res.json value is :", res.json)
    print("res.json().get(\"email\") value is: ", res.json().get("email"))
    assert res.json().get("email") == "amit_5@gmail.com"
    assert res.status_code == 201

    # Lets check if the created user has all the values which UserCreationResponse has.
    new_user = Schemas.UserCreationResponse(
        **res.json())  # doing a pydantic validation
    print(Schemas.UserCreationResponse(**res.json()))
    assert new_user.email == "amit_5@gmail.com"

from jose import jwt
from FastAPIDemo.config import setting
def test_login_user(client, test_user):
    #print("the username & password is: ", test_user['email'], test_user['password'])
    res= client.post("/login", data={"username": test_user['email'], "password": test_user['password']}) 
    # I used data instead of json because we are asking to enter the values ina form request not in json
    # Also i used email value in "username" for the login form data, so I thats why I have provided username not email
    assert res.status_code == 200

    #Validating the access token:
    print("Value of JSON is :",res.json())
    login_res = Schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'


@pytest.mark.parametrize("email, password, status_code", [(
    'wrongemail@gmail.com', 'test', 403), 
    ('test@gmail.com', 'wrongpassword', 403), 
    ('wrongemail@gmail.com', 'wrongpassword', 403), 
    (None, 'test', 422), ('test@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
