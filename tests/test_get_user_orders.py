import allure

from api.order_api import OrderApi


class TestGetUserOrders:

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_authorized_user_success(
        self, created_user_with_order
    ):
        token = created_user_with_order['token']

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