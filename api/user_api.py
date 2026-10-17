import allure
import requests

from urls import CREATE_USER_URL, LOGIN_USER_URL, USER_URL


class UserApi:

    @staticmethod
    @allure.step('Создать пользователя')
    def create_user(data):
        return requests.post(CREATE_USER_URL, json=data)

    @staticmethod
    @allure.step('Авторизовать пользователя')
    def login_user(data):
        return requests.post(LOGIN_USER_URL, json=data)

    @staticmethod
    @allure.step('Изменить данные пользователя')
    def update_user(data, token=None):
        headers = {}

        if token:
            headers['Authorization'] = token

        return requests.patch(USER_URL, json=data, headers=headers)

    @staticmethod
    @allure.step('Удалить пользователя')
    def delete_user(token):
        headers = {
            'Authorization': token
        }

        return requests.delete(USER_URL, headers=headers)