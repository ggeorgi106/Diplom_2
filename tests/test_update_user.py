import allure

from api.user_api import UserApi
from helpers import generate_random_string


class TestUpdateUser:

    @allure.title('Изменение email авторизованного пользователя')
    def test_update_email_authorized_user_success(self, created_user):
        token = created_user['token']

        new_email = f'{generate_random_string(10)}@yandex.ru'
        update_data = {
            'email': new_email
        }

        response = UserApi.update_user(update_data, token)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == new_email

    @allure.title('Изменение имени авторизованного пользователя')
    def test_update_name_authorized_user_success(self, created_user):
        token = created_user['token']

        new_name = generate_random_string(10)
        update_data = {
            'name': new_name
        }

        response = UserApi.update_user(update_data, token)

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['name'] == new_name

    @allure.title('Нельзя изменить данные пользователя без авторизации')
    def test_update_user_without_authorization_error(self):
        update_data = {
            'name': generate_random_string(10)
        }

        response = UserApi.update_user(update_data)

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'You should be authorised'