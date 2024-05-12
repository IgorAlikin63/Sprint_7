import requests
import allure
import urls

class TestGetOrdersList:

    @allure.title("Проверка получения списка заказов на бронирование")
    @allure.description(
        "Тест проверяет, что можно получить список всех бронирований")

    def test_get_orders_list_not_empty(self):

        with allure.step("Вызываем ручку списка бронирований"):
                response_get_orders_list_not_empty = requests.get(
                urls.BASE_URL + urls.ORDERS_LIST)

        with allure.step("Проверяем код ответа"):
            assert response_get_orders_list_not_empty.status_code == 200

        with allure.step("Проверяем, что ответ не пустой"):
            assert response_get_orders_list_not_empty.json() is not None