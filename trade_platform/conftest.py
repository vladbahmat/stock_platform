import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture(autouse=True)
def access_db(db):
    pass


@pytest.fixture
def get_token(db):
    client = APIClient()
    u = User.objects.create_user(username='admin', password='admin')
    u.save()
    response = client.post('http://0.0.0.0:8000/trade_platform/login', {"username": "admin", "password": "admin"},
                           format='json')
    return response.data['access']


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def login(client, get_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(get_token))


