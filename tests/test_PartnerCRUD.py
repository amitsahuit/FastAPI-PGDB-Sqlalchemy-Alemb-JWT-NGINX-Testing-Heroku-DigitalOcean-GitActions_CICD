import pytest
from FastAPIDemo import Schemas


def test_get_all_partner(authorized_client, test_partner):
    res = authorized_client.get("/partners/")
    # def validate(post):
    #     return schemas.PostOut(**post)
    # posts_map = map(validate, res.json())
    # posts_list = list(posts_map)
    print("The Json value of all partner list is: ",res.json())
    assert res.status_code == 200

def test_unauthorized_user_get_all_partner(client, test_partner):
    res = client.get("/partners/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_partner(client, test_partner):
    res = client.get(f"/partners/{test_partner[0].id}")
    assert res.status_code == 401


def test_get_one_partner_not_exist(authorized_client, test_partner):
    res = authorized_client.get(f"/partners/88888")
    assert res.status_code == 404


def test_get_one_partner(authorized_client, test_partner):
    res = authorized_client.get(f"/partners/{test_partner[0].id}")
    print(res.json())
    
    # Doing Validation
    partner = Schemas.PartnerResponseSchema(**res.json())
    print("Unpacked Partner values are: ",partner)
    assert partner.id == test_partner[0].id
    assert partner.partnername == test_partner[0].partnername
    assert partner.partnerfunction == test_partner[0].partnerfunction


@pytest.mark.parametrize("partnername, partnerfunction, rating, published", [
    ("partner1", "Seller", 4, True),
    ("partner2", "Seller", 4, False),
    ("partner3", "Seller", 4, True),
])
def test_create_partner(authorized_client, test_user, test_partner, partnername, partnerfunction, rating, published):
    res = authorized_client.post("/partners/", json={"partnername": partnername, "partnerfunction": partnerfunction, "rating": rating, "published": published})
    #print("Value of responce inside test_create_partner is:",res.json())
    created_partner = Schemas.PartnerResponseSchema(**res.json())
    assert res.status_code == 201
    assert created_partner.partnername == partnername
    assert created_partner.partnerfunction == partnerfunction
    assert created_partner.rating == rating
    # assert created_partner.published == published
    assert created_partner.owner_id == test_user['id']


def test_create_partner_default_rating_4(authorized_client, test_user, test_partner):
    res = authorized_client.post(
        "/partners/", json={"partnername": "partner1", "partnerfunction": "seller", "rating": 4})

    created_partner = Schemas.PartnerResponseSchema(**res.json())
    assert res.status_code == 201
    assert created_partner.partnername == "partner1"
    assert created_partner.partnerfunction == "seller"
    assert created_partner.rating == 4
    assert created_partner.owner_id == test_user['id']


def test_unauthorized_user_create_partner(client, test_user, test_partner):
    res = client.post(
        "/partners/", json={"partnername": "partner1", "partnerfunction": "seller"})
    assert res.status_code == 401


def test_unauthorized_user_delete_partner(client, test_user, test_partner):
    res = client.delete(
        f"/partners/{test_partner[0].id}")
    assert res.status_code == 401


def test_delete_partner_success(authorized_client, test_user, test_partner):
    res = authorized_client.delete(
        f"/partners/{test_partner[0].id}")

    assert res.status_code == 204


def test_delete_partner_non_exist(authorized_client, test_user, test_partner):
    res = authorized_client.delete(
        f"/partners/8000000")

    assert res.status_code == 404


def test_delete_other_user_partner(authorized_client, test_user, test_partner):
    res = authorized_client.delete(
        f"/partners/{test_partner[3].id}")
    assert res.status_code == 403


def test_update_partner(authorized_client, test_user, test_partner):
    data = {
        "partnername": "updated partnername",
        "partnerfunction": "updatd partnerfunction",
        "id": test_partner[0].id

    }
    res = authorized_client.put(f"/partners/{test_partner[0].id}", json=data)
    updated_partner = Schemas.createPartner(**res.json())
    assert res.status_code == 200
    assert updated_partner.partnername == data['partnername']
    assert updated_partner.partnerfunction == data['partnerfunction']


def test_update_other_user_partner(authorized_client, test_user, test_user2, test_partner):
    data = {
        "partnername": "updated partnername",
        "partnerfunction": "updatd partnerfunction",
        "id": test_partner[3].id

    }
    res = authorized_client.put(f"/partners/{test_partner[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_partner(client, test_user, test_partner):
    res = client.put(
        f"/partners/{test_partner[0].id}")
    assert res.status_code == 401


def test_update_partner_non_exist(authorized_client, test_user, test_partner):
    data = {
        "partnername": "updated partnername",
        "partnerfunction": "updatd partnerfunction",
        "id": test_partner[3].id

    }
    res = authorized_client.put(
        f"/partners/80000000", json=data)
    assert res.status_code == 403
#    assert res.status_code == 404