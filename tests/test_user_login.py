import requests
import allure
import urls
import pytest
import data

class TestCourierlogin:

    @allure.title("Проверка успешной авторизации существующим курьеров")
    @allure.description(
        "Тест проверяет, что можно авторизоваться уже существующим курьером")

    def test_courier_can_auth_with_existing_credentials(self):

        with allure.step("Формируем payload используя данные о существующем курьере из data"):
            payload = data.TestCourierAuth.AUTH_COURIER_BODY

        with allure.step("Вызываем ручку авторизации со сформированным payload"):
            response = requests.post(
                urls.BASE_URL + urls.COURIER_LOGIN, json=payload)

        with allure.step("Проверяем код ответа и наличие в ответе id"):
            assert response.status_code == 200 and response.json()['id'] is not None

    @pytest.mark.parametrize('missing_field, '
                             'error_message', [
                                 ('login', 'Недостаточно данных для создания учетной записи'),
                                 ('password', 'Недостаточно данных для создания учетной записи')])
    @allure.title("Проверка невозможности авторизоваться с пустым значением в обязательом поле")
    @allure.description(
        "Тест проверяет, что невозможно авторизоваться с пустым значением в обязательом поле логин/пароль")

    def test_courier_cant_auth_without_required_fields(self, missing_field, error_message):

        with allure.step("Создаем копию тела запроса с верными данными о курьере перед изменениями"):
            payload = data.TestCourierAuth.AUTH_COURIER_BODY.copy()

        with allure.step("В payload заменяем одно из значений на пустое"):
            payload[missing_field] = ''

        with allure.step("Вызываем ручку авторизации со сформированным payload"):
            response_without_required_fields = requests.post(
                urls.BASE_URL + urls.COURIER_LOGIN, json=payload)

        with allure.step("Проверяем код ответа"):
            assert response_without_required_fields.status_code == 400

        with allure.step("Проверяем сообщение из ответа"):
            assert response_without_required_fields.json()['message'] == "Недостаточно данных для входа"

    @allure.title("Проверка невозможности авторизоваться за незарегистрированного пользователя")
    @allure.description(
        "Тест проверяет, что невозможно авторизоваться за пользователя, который не прошел регистрацию")

    def test_failed_login_attempt_with_unregistered_login_password(self):

        with allure.step("Создаем payload с данными курьера, который не регистрировался и хранится в data"):
            payload = data.TestUnregisteredCourierCredentials.AUTH_WITH_UNREGISTERED_COURIER_BODY

        with allure.step("Пытаемся авторизоваться с этим payloaf"):
            response_with_unregistered_login_password = requests.post(
                urls.BASE_URL + urls.COURIER_LOGIN, json=payload)

        with allure.step("Проверяем код ответа"):
            assert response_with_unregistered_login_password.status_code == 404

        with allure.step("Проверяем сообщение из ответа"):
            assert response_with_unregistered_login_password.json()['message'] == "Учетная запись не найдена"


