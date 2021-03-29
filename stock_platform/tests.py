# import pytest
# from django.contrib.auth.models import User
# from django.urls import reverse
# from rest_framework.test import APIClient
#
#
# @pytest.mark.django_db
# def test_my_user():
#     User.objects.create_user('test', 'password')
#     assert User.objects.count() == 1
#
#
# @pytest.mark.django_db
# def test_airport_list_real():
#     client = APIClient()
#     response = client.get(reverse('/trade_platform/item'))
#     assert response.status_code == 200
#     assert len(response.json()) > 0
