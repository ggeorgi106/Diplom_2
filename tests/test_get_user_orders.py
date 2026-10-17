import allure
import requests

from api.order_api import OrderApi
from api.user_api import UserApi
from helpers import generate_user_data
from urls import INGREDIENTS_URL


class TestGetUserOrders:

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_authorized_user_success(self, user_cleanup):
        user_data = generate_user_data()

        create_response = UserApi.create_user(user_data)

        assert create_response.status_code == 200

        token = create_response.json()['accessToken']
        user_cleanup.append({'token': token})

        ingredients_response = requests.get(INGREDIENTS_URL)
        ingredients = ingredients_response.json()['data']

        order_data = {
            'ingredients': [
                ingredients[0]['_id'],
                ingredients[1]['_id']
            ]
        }

        order_response = OrderApi.create_order(order_data, token)
        assert order_response.status_code == 200

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