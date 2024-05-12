import requests
import urls
import random
import string
import allure

class CourierApi:

    @staticmethod
    @allure.step('Создаем случайную строку определенной длины')

    def generate_random_string(length):

        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @allure.step('Регистрируем нового курьера со случайными данными, возвращаем словарь с его именем, логином, паролем')

    def register_new_courier_and_return_login_password():

        # генерируем логин, пароль и имя курьера
        login = CourierApi.generate_random_string(10)
        password = CourierApi.generate_random_string(10)
        first_name = CourierApi.generate_random_string(10)

        # собираем тело запроса
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post(urls.BASE_URL + urls.COURIER_CREATION, json=payload)

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if response.status_code == 201:
            return {
                "login": login,
                "password": password,
                "firstName": first_name
                }

        # возвращаем словарь
        return {}

    @staticmethod
    @allure.step('Авторизуем курьера и получаем его id')
    def login_courier_and_get_id(login, password):
        login_payload = {
            "login": login,
            "password": password
        }
        response_login = requests.post(urls.BASE_URL + urls.COURIER_LOGIN, json=login_payload)
        if response_login.status_code == 200:
            return response_login.json()['id']
        else:
            return None

    @staticmethod
    @allure.step('Удаляем курьера по id')
    def delete_courier_by_id(courier_id):
        delete_endpoint = urls.DELETE_COURIER.replace('id', str(courier_id))
        response_delete = requests.delete(urls.BASE_URL + delete_endpoint)
        if response_delete.status_code == 200:
            return True
        else:
            return False
