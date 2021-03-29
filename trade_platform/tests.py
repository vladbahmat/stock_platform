import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from trade_platform.serializers import ItemSerializer
from trade_platform.conftest import access_db
from trade_platform.models import Item


def test_my_user():
    User.objects.create_user('test', 'password')
    assert User.objects.count() == 1


def test_item_create(client, login):
    """Creating item with good data"""
    url = '/trade_platform/item/'
    data = {'name':'test', 'code':'test'}
    response = client.post(url, data, format='json')
    assert response.status_code == 201


def test_item_create_unique(client, login):
    """Creating item with not unique data"""
    url = '/trade_platform/item/'
    data = {'name': 'test', 'code': 'test'}
    response = client.post(url, data, format='json')
    response = client.post(url, data, format='json')
    assert response.status_code == 400


def test_item_list( client, login):
    url = '/trade_platform/item/'
    response = client.get(url)
    assert response.status_code == 200
    client.credentials(HTTP_AUTHORIZATION='Bearer testtoken')
    response = client.get(url)
    assert response.status_code == 401


def test_auth(client):
    u = User.objects.create_user(username='admin', password='admin')
    u.save()
    response = client.post('http://0.0.0.0:8000/trade_platform/login', {"username": "admin", "password": "admin"},
                           format='json')
    assert response.status_code == 200
    response = client.post('http://0.0.0.0:8000/trade_platform/login', {"username": "bad", "password": "admin"},
                           format='json')
    assert response.status_code == 401
