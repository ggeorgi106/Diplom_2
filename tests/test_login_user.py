import allure

from api.user_api import UserApi
from helpers import generate_user_data


class TestLoginUser:

    @allure.title('Авторизация существующего пользователя')
    def test_login_existing_user_success(self):
        user_data = generate_user_data()
        UserApi.create_user(user_data)

        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }

        response = UserApi.login_user(login_data)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()

    @allure.title('Авторизация с неверным логином и паролем')
    def test_login_user_with_invalid_credentials_error(self):
        login_data = {
            'email': 'invalid_user@yandex.ru',
            'password': 'invalid_password'
        }

        response = UserApi.login_user(login_data)

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'