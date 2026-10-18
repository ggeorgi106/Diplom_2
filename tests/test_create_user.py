import allure
import pytest

from api.user_api import UserApi
from helpers import generate_user_data


class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user_success(self, user_cleanup):
        user_data = generate_user_data()

        response = UserApi.create_user(user_data)

        if response.status_code == 200:
            user_cleanup.append(user_data)

        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Нельзя создать двух одинаковых пользователей')
    def test_create_duplicate_user_error(self, created_user):
        user_data = {
            'email': created_user['email'],
            'password': created_user['password'],
            'name': created_user['name']
        }

        response = UserApi.create_user(user_data)

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'

    @allure.title('Нельзя создать пользователя без обязательного поля')
    @pytest.mark.parametrize(
        'missing_field',
        ['email', 'password', 'name']
    )
    def test_create_user_without_required_field_error(
        self, missing_field
    ):
        user_data = generate_user_data()
        user_data.pop(missing_field)

        response = UserApi.create_user(user_data)

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == (
            'Email, password and name are required fields'
        )