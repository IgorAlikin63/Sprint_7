import pytest
from courier_api import CourierApi
import allure

@pytest.fixture(scope='function')
@allure.step('Генерируем нового курьера для теста, авторизуем его, удаляем тестовые данные')

def new_courier_creation(request):

    courier_data = CourierApi.register_new_courier_and_return_login_password()

    def delete_courier():
        # Авторизуемся созданным курьером для получения его id
        courier_id = CourierApi.login_courier_and_get_id(courier_data['login'], courier_data['password'])
        assert courier_id, "Не удалось получить id курьера"

        # Удаляем курьера по id
        assert CourierApi.delete_courier_by_id(courier_id), "Не удалось удалить курьера"

    request.addfinalizer(delete_courier)
    return courier_data




