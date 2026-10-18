import allure
import pytest
import requests

from api.order_api import OrderApi
from urls import INGREDIENTS_URL


@pytest.fixture
def order_ingredients():
    response = requests.get(INGREDIENTS_URL)

    if response.status_code != 200:
        pytest.fail('Не удалось получить ингредиенты')

    ingredients = response.json()['data']

    if len(ingredients) < 2:
        pytest.fail('Недостаточно ингредиентов для теста')

    return {
        'ingredients': [
            ingredients[0]['_id'],
            ingredients[1]['_id']
        ]
    }


class TestCreateOrder:

    @allure.title('Создание заказа с авторизацией')
    def test_create_order_authorized_user_success(
        self, created_user, order_ingredients
    ):
        token = created_user['token']

        response = OrderApi.create_order(
            order_ingredients,
            token
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'order' in response.json()

    @allure.title('Создание заказа без авторизации')
    def test_create_order_unauthorized_user_success(
        self, order_ingredients
    ):
        response = OrderApi.create_order(order_ingredients)

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
        assert response.json()['message'] == (
            'Ingredient ids must be provided'
        )

    @allure.title('Нельзя создать заказ с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash_error(self):
        order_data = {
            'ingredients': ['invalid_ingredient_hash']
        }

        response = OrderApi.create_order(order_data)

        assert response.status_code == 500