import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient

from base.models import Product

'''
Unit tests -> checking user creation func
'''
@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('test','test@test.com','test')
    count = User.objects.all().count()
    assert count == 1

@pytest.fixture()
def user_1(db):
    return User.objects.create_user("test-user")

@pytest.mark.django_db
def test_set_check_password(user_1):
    user_1.set_password("new-password")
    assert user_1.check_password("new-password") is True



'''
Integration testing testing api to register user
'''
@pytest.mark.django_db
def test_register_user():
    client = APIClient()

    payload = dict(
        name="testing123",
        email="test11@test.com",
        password="super-secret"
    )

    response = client.post("/api/users/register/", payload)

    data = response.data

    assert data["name"] == payload["name"]