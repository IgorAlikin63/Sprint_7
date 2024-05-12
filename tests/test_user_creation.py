import requests
from courier_api import CourierApi
import urls
import pytest
import data
import allure

class TestNewCourierCreation:
    @allure.title("Проверка успешного создания курьера через фикстуру")
    @allure.description(
        "Тест проверяет, что после отработки фикстуры словарь содержит имя, логин, пароль курьера")

    def test_new_courier_creation_success(self, new_courier_creation):

        with allure.step("Проверка, что фикстура отработала"):
            assert new_courier_creation, "Не удалось создать курьера"

        with allure.step("Проверка, что словарь содержит логин"):
            assert "login" in new_courier_creation, "Нет логина в данных нового курьера"

        with allure.step("Проверка, что словарь содержит пароль"):
            assert "password" in new_courier_creation, "Нет пароля в данных нового курьера"

        with allure.step("Проверка, что словарь содержит имя"):
            assert "firstName" in new_courier_creation, "Нет имени в данных нового курьера"

    @allure.title("Проверка, что нельзя создать двух одинаковых курьеров с одинаковыми данными")
    @allure.description(
        "Тест проверяет, что создать двух курьеров с одинаковыми данными невозможно, будет ошибка")

    def test_cant_create_two_couriers_with_same_data_and_get_error(self, new_courier_creation):

        with allure.step("Создаем payload, который является копией фикстуры new_courier_creation"):
            payload = new_courier_creation.copy()

        with allure.step("Отправляем повторно payload на ручку создания курьера"):
            response_with_same_data = requests.post(
                urls.BASE_URL + urls.COURIER_CREATION, json=payload)

        with allure.step("Проверяем соответствие кода из ответа ручки"):
            assert response_with_same_data.status_code == 409

        with allure.step("Проверяем соответствие сообщения об ошибке"):
            assert response_with_same_data.json()['message'] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize('missing_field, '
                             'error_message', [
        ('login', 'Недостаточно данных для создания учетной записи'),
        ('password', 'Недостаточно данных для создания учетной записи'),
        ('firstName', 'Недостаточно данных для создания учетной записи')
    ])
    @allure.title("Проверка, что нельзя создать курьера без обязательных полей")
    @allure.description(
        "Тест проверяет, что нельзя создать курьера без обязательных полей, будет ошибка")

    def test_cant_create_courier_without_required_fields_and_get_error(self, missing_field, error_message):

        with allure.step("В payload сохранили заготовленный шаблон создания курьера из data, содержащий все необходимые поля"):
            payload = data.TestDataForCourierCreation.CREATE_COURIER_BODY

        with allure.step("В payload удаляем одно из полей"):
            del payload[missing_field]

        with allure.step("Отправляем payload с отсутствующим полем на ручку создания курьера"):
            response_without_required_fields = requests.post(
                urls.BASE_URL + urls.COURIER_CREATION, json=payload)

        with allure.step("Проверяем код из ответа ручки"):
            assert response_without_required_fields.status_code == 400

        with allure.step("Проверяем соответствие сообщения об ошибке"):
            assert response_without_required_fields.json()['message'] == "Недостаточно данных для создания учетной записи"

    @allure.title("Проверка тела ответа и кода при успешной регистрации")
    @allure.description("Тест проверяет, что при успешной регистрации курьера тело ответа будет содержать соответствующий json и код ответа")

    def test_status_code_and_json_body_check_for_successfull_registration(self):

        with allure.step("Создаем случайные значения параметров имя, логин, пароль для курьера используя функцию случайной строки"):
            login = CourierApi.generate_random_string(10)
            password = CourierApi.generate_random_string(10)
            first_name = CourierApi.generate_random_string(10)

        with allure.step(
                "Создаем payload для ручки создания курьера"):
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }

        with allure.step(
                "Создаем курьера, используя сформированный payload"):
            response = requests.post(urls.BASE_URL + urls.COURIER_CREATION, json=payload)

        with allure.step("Проверяем код из ответа ручки"):
            assert response.status_code == 201

        with allure.step("Проверяем тело ответа ручки"):
            assert response.json() == {"ok": True}

    @allure.title("Проверка, что нельзя создать курьера с тем же логином дважды")
    @allure.description(
        "Тест проверяет, что при попытке создать курьера с уже существующим логином невозможно, будет ошибка")

    def test_cant_create_courier_with_same_login(self):

        with allure.step("Создаем случайные значения параметров имя, логин, пароль для курьера используя функцию случайной строки"):
            login = CourierApi.generate_random_string(10)
            password = CourierApi.generate_random_string(10)
            first_name = CourierApi.generate_random_string(10)

        with allure.step("Создаем payload для ручки создания курьера"):
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }

        with allure.step("Создаем курьера, используя сформированный payload"):
            response = requests.post(urls.BASE_URL + urls.COURIER_CREATION, json=payload)

        with allure.step(
                "Проверяем успешность создания"):
            assert response.status_code == 201

        with allure.step(
                "Создаем новые случайные значения параметров имя, пароль для курьера используя функцию случайной строки"):
            new_password = CourierApi.generate_random_string(10)
            new_first_name = CourierApi.generate_random_string(10)

        with allure.step("Создаем новый payload для ручки создания курьера, используя старый логин и новые имя, пароль"):
            new_payload_with_same_login = {
                "login": login,
                "password": new_password,
                "firstName": new_first_name
            }

        with allure.step("Создаем курьера, используя новый сформированный payload"):
            new_response = requests.post(urls.BASE_URL + urls.COURIER_CREATION, json=new_payload_with_same_login)

        with allure.step("Проверяем код из ответа ручки"):
            assert new_response.status_code == 409

        with allure.step("Проверяем сообщение из ответа ручки"):
            assert new_response.json()['message'] == "Этот логин уже используется. Попробуйте другой."



