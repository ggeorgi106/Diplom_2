import allure

from api.user_api import UserApi


class TestLoginUser:

    @allure.title('Авторизация существующего пользователя')
    def test_login_existing_user_success(self, created_user):
        login_data = {
            'email': created_user['email'],
            'password': created_user['password']
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