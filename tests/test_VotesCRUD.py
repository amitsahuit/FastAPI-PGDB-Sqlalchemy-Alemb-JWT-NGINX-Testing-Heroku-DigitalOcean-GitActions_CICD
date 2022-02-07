import pytest
from FastAPIDemo import models


@pytest.fixture()
def test_vote(test_partner, session, test_user):
    new_vote = models.Vote(partner_id=test_partner[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_partner(authorized_client, test_partner):
    res = authorized_client.post(
        "/vote/", json={"partner_id": test_partner[3].id, "direction": 1})
    assert res.status_code == 201


def test_vote_twice_partner(authorized_client, test_partner, test_vote):
    res = authorized_client.post(
        "/vote/", json={"partner_id": test_partner[3].id, "direction": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_partner, test_vote):
    res = authorized_client.post(
        "/vote/", json={"partner_id": test_partner[3].id, "direction": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_partner):
    res = authorized_client.post(
        "/vote/", json={"partner_id": test_partner[3].id, "direction": 0})
    assert res.status_code == 404


#ForeignKeyViolation
# def test_vote_partner_non_exist(authorized_client, test_partner):
#     res = authorized_client.post(
#         "/vote/", json={"partner_id": 60, "direction": 1})
#     print("test_vote_unauthorized_user response code is: ",res.status_code)
#     assert res.status_code == 404


def test_vote_unauthorized_user(client, test_partner):
    res = client.post(
        "/vote/", json={"partner_id": test_partner[3].id, "direction": 1})
    assert res.status_code == 401