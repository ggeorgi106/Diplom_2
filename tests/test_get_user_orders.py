import allure

from api.order_api import OrderApi
from api.user_api import UserApi
from helpers import generate_user_data
from urls import INGREDIENTS_URL

import requests


class TestGetUserOrders:

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_authorized_user_success(self):
        user_data = generate_user_data()
        UserApi.create_user(user_data)

        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }

        login_response = UserApi.login_user(login_data)
        token = login_response.json()['accessToken']

        ingredients_response = requests.get(INGREDIENTS_URL)
        ingredients = ingredients_response.json()['data']

        order_data = {
            'ingredients': [
                ingredients[0]['_id'],
                ingredients[1]['_id']
            ]
        }

        OrderApi.create_order(order_data, token)

        response = OrderApi.get_user_orders(token)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'orders' in response.json()
        assert len(response.json()['orders']) > 0

    @allure.title('Нельзя получить заказы без авторизации')
    def test_get_orders_unauthorized_user_error(self):
        response = OrderApi.get_user_orders()

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'You should be authorised'