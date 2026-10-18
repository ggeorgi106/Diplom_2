import pytest
import requests

from api.order_api import OrderApi
from api.user_api import UserApi
from helpers import generate_user_data
from urls import INGREDIENTS_URL


@pytest.fixture
def user_cleanup():
    created_users = []

    yield created_users

    for user_data in created_users:
        token = user_data.get('token')

        if not token:
            response = UserApi.login_user({
                'email': user_data['email'],
                'password': user_data['password']
            })

            if response.status_code != 200:
                continue

            token = response.json().get('accessToken')

        if token:
            UserApi.delete_user(token)


@pytest.fixture
def created_user(user_cleanup):
    user_data = generate_user_data()
    response = UserApi.create_user(user_data)

    if response.status_code != 200:
        pytest.fail(
            f'Не удалось создать тестового пользователя: '
            f'{response.status_code}'
        )

    token = response.json().get('accessToken')

    user_cleanup.append({
        'token': token,
        'email': user_data['email'],
        'password': user_data['password']
    })

    return {
        'email': user_data['email'],
        'password': user_data['password'],
        'name': user_data['name'],
        'token': token
    }


@pytest.fixture
def created_user_with_order(created_user):
    token = created_user['token']

    ingredients_response = requests.get(INGREDIENTS_URL)

    if ingredients_response.status_code != 200:
        pytest.fail('Не удалось получить ингредиенты для заказа')

    ingredients = ingredients_response.json()['data']

    order_data = {
        'ingredients': [
            ingredients[0]['_id'],
            ingredients[1]['_id']
        ]
    }

    order_response = OrderApi.create_order(order_data, token)

    if order_response.status_code != 200:
        pytest.fail(
            f'Не удалось создать тестовый заказ: '
            f'{order_response.status_code}'
        )

    return created_user