import requests
import allure
import urls
import pytest
import data

class TestScooterOrderCreation:

    @pytest.mark.parametrize('color', ['BLACK', 'GREY', 'BLACK, GREY', ''])
    @allure.title("Проверка создания заказа на бронирование самоката с разными цветами")
    @allure.description(
        "Тест проверяет, что можно забронировать самокат черный, серый, черный и серый, не указывая цвет")

    def test_scooter_order_with_variable_colours(self, color):

        with allure.step("Формируем payload используя данные о базовом бронировании самоката из data"):
            payload = data.TestBaseScooterOrder.BASE_SCOOTER_ORDER.copy()
        with allure.step("Обрабатываем цвет из параметризации"):
            payload['color'] = color.split(', ') if color else []

        with allure.step("Вызываем ручку бронирования с использованием сформированного payload"):
            response_with_variable_colours = requests.post(
                urls.BASE_URL + urls.ORDER_CREATION, json=payload)

        with allure.step("Проверяем код ответа"):
            assert response_with_variable_colours.status_code == 201

        with allure.step("Проверяем наличие в ответе поля 'track' и что ему присвоено значение больше 0"):
            assert 'track' in response_with_variable_colours.json() and response_with_variable_colours.json()['track'] > 0