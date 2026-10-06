import allure
import requests

from urls import CREATE_ORDER_URL


class OrderApi:

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(data, token=None):
        headers = {}

        if token:
            headers['Authorization'] = token

        return requests.post(
            CREATE_ORDER_URL,
            json=data,
            headers=headers
        )

    @staticmethod
    @allure.step('Получить заказы пользователя')
    def get_user_orders(token=None):
        headers = {}

        if token:
            headers['Authorization'] = token

        return requests.get(
            CREATE_ORDER_URL,
            headers=headers
        )