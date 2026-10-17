import pytest

from api.user_api import UserApi


@pytest.fixture
def user_cleanup():
    created_users = []

    yield created_users

    for user_data in created_users:
        token = user_data.get('token')

        if not token:
            response = UserApi.login_user({
                'email': user_data['email'],
                'password': user_data['password']
            })

            assert response.status_code == 200, (
                'Не удалось авторизовать пользователя для удаления'
            )

            token = response.json().get('accessToken')

        assert token, 'Не удалось получить токен для удаления пользователя'

        delete_response = UserApi.delete_user(token)

        assert delete_response.status_code == 202, (
            f'Не удалось удалить пользователя: '
            f'{delete_response.status_code}'
        )