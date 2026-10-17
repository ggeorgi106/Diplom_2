import allure
import requests

from api.order_api import OrderApi
from api.user_api import UserApi
from helpers import generate_user_data
from urls import INGREDIENTS_URL


class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией')
    def test_create_order_authorized_user_success(self, user_cleanup):
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

        response = OrderApi.create_order(
            order_data,
            token
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Создание заказа без авторизации')
    def test_create_order_unauthorized_user_success(self):
        ingredients_response = requests.get(INGREDIENTS_URL)
        ingredients = ingredients_response.json()['data']

        order_data = {
            'ingredients': [
                ingredients[0]['_id'],
                ingredients[1]['_id']
            ]
        }

        response = OrderApi.create_order(order_data)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Нельзя создать заказ без ингредиентов')
    def test_create_order_without_ingredients_error(self):
        order_data = {
            'ingredients': []
        }

        response = OrderApi.create_order(order_data)

        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Нельзя создать заказ с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash_error(self):
        order_data = {
            'ingredients': ['invalid_ingredient_hash']
        }

        response = OrderApi.create_order(order_data)

        assert response.status_code == 500