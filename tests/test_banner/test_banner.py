import pytest
import requests


@pytest.fixture
def user_token():
    response = requests.post("http://127.0.0.1:8000/auth/jwt/login",
                             data={
                                 "username": "admin@mail.com",
                                 "password": "admin"
                             })
    token = response.json()["access_token"]
    return token


@pytest.mark.order1
def test_add_feature(user_token):
    print(user_token)
    response = requests.post("http://127.0.0.1:8000/feature",
                             headers={
                                 "Authorization": f"Bearer {user_token}"},
                             json={
                                 "name": "string"
                             })
    assert response.status_code == 200


@pytest.mark.order2
def test_add_tag(user_token):
    response = requests.post("http://127.0.0.1:8000/tag",
                             headers={
                                 "Authorization": f"Bearer {user_token}"},
                             json={
                                 "name": "string"
                             })
    assert response.status_code == 200


@pytest.mark.order3
def test_add_banner(user_token):
    response = requests.post("http://127.0.0.1:8000/banner",
                             headers={
                                 "Authorization": f"Bearer {user_token}"},
                             json={
                                 "feature_id": 1,
                                 "content": {},
                                 "is_active": True,
                                 "tag_ids": [
                                     1
                                 ]
                             })
    assert response.status_code == 200


@pytest.mark.order4
def test_get_banner(user_token):
    response = requests.get("http://127.0.0.1:8000/"
                            "user_banner?tag_id=1&feature_id=1&use_last_revision=true",
                            headers={
                                "Authorization": f"Bearer {user_token}"}
                            )
    assert response.status_code == 200
