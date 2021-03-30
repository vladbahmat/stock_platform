import pytest

from rest_framework.test import APIClient
from django.contrib.auth.models import User

from trade_platform.models import Item, Profile


@pytest.fixture(autouse=True)
def access_db(db):
    pass


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='admin', password='admin')
    user.save()
    return user

@pytest.fixture
def get_token(db, client, create_user):
    response = client.post('http://0.0.0.0:8000/trade_platform/login', {"username": "admin", "password": "admin"},
                           format='json')
    return response.data['access']


@pytest.fixture
def login(client, get_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(get_token))


@pytest.fixture
def item_data():
    data = {'name': 'test', 'code': 'test'}
    return data


@pytest.fixture
def create_item(item_data):
    item = Item.objects.create(name='test', code='test')
    item.save()
    return item

