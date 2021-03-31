from django.contrib.auth.models import User


def test_my_user(create_user):
    """Testing creating 1 User"""
    assert User.objects.count() == 1


def test_watchlist_list(client, login):
    """Testing watchlist list method"""
    url = '/trade_platform/watchlist/'
    response = client.get(url)
    assert response.status_code == 200


def test_watchlist_retrieve(client, login, create_user):
    """Testing watchlist retrieve method"""
    response = client.get('/trade_platform/watchlist/{}/'.format(create_user.id))
    assert response.status_code == 200
    response = client.get('/trade_platform/watchlist/115/')
    assert response.status_code == 404


def test_watchlist_update(client, login, create_user, create_item):
    """Add new item, then update this item"""
    user = create_user
    item_before = user.profile.watchlist
    new_data = {'item': [create_item.id]}
    response = client.patch('/trade_platform/watchlist/{}/'.format(user.id), new_data, format='json')
    item_after = response.data
    assert response.status_code == 200
    assert item_before != item_after


def test_offer_create(client, login, create_user, create_item):
    """Test creating offer with different quantity values"""
    url = '/trade_platform/offer/'
    data = {"item": create_item.id, "quantity": 20}
    response = client.post(url, data, format='json')
    assert response.status_code == 400  #can't create offer with more than 10 item one time
    data = {"item": create_item.id, "quantity": 15}
    response = client.post(url, data, format='json')
    assert response.status_code == 201


def test_offer_list(client, login, create_item):
    url = '/trade_platform/offer/'
    response = client.get(url)
    assert response.status_code == 200


def test_offer_retrieve(client, login, create_user, create_item):
    url = '/trade_platform/offer/'
    data = {"item": create_item.id, "quantity": 5}
    response = client.post(url, data, format='json')
    #print(response.data)
    response = client.get('/trade_platform/offer/{}/'.format(response.data['id']))
    assert response.status_code == 200


def test_item_create(client, login, item_data):
    """Creating item with good data"""
    url = '/trade_platform/item/'
    response = client.post(url, item_data, format='json')
    assert response.status_code == 201


def test_item_create_unique(client, login, item_data):
    """Creating item with not unique data"""
    url = '/trade_platform/item/'
    response = client.post(url, item_data, format='json')
    response = client.post(url, item_data, format='json')
    assert response.status_code == 400


def test_item_update(client, login, item_data):
    """Add new item, then update this item"""
    url = '/trade_platform/item/'
    response = client.post(url, item_data, format='json')
    item_before = response.data
    new_data = {'name': 'test1', 'code': 'test1'}
    response = client.patch('/trade_platform/item/{0}/'.format(response.data['id']), new_data)
    item_after = response.data
    assert response.status_code == 200
    assert item_before != item_after


def test_item_list(client, login):
    """Show item's list"""
    url = '/trade_platform/item/'
    response = client.get(url)
    assert response.status_code == 200


def test_authorisation(client):
    """Authorisation with bad access token"""
    client.credentials(HTTP_AUTHORIZATION='Bearer badtoken')
    url = '/trade_platform/item/'
    response = client.get(url)
    assert response.status_code == 401


def test_login(client):
    """Testing authorisation"""
    u = User.objects.create_user(username='admin', password='admin')
    u.save()
    response = client.post('http://0.0.0.0:8000/trade_platform/login', {"username": "admin", "password": "admin"},
                           format='json')
    assert response.status_code == 200
    response = client.post('http://0.0.0.0:8000/trade_platform/login', {"username": "bad", "password": "admin"},
                           format='json')
    assert response.status_code == 401
