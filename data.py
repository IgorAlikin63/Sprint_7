class TestDataForCourierCreation:
    CREATE_COURIER_BODY = {
        "login": "courier_seven",
        "password": "1234",
        "firstName": "courier"
        }

class TestDataAlreadyRegistered:
    ALREADY_REGISTERED = {
        "login": "courier_eleven",
        "password": "1234",
        "firstName": "courier"
        }

class TestCourierAuth:
    AUTH_COURIER_BODY = {
        "login": "courier_six",
        "password": "1234"
        }

class TestUnregisteredCourierCredentials:
    AUTH_WITH_UNREGISTERED_COURIER_BODY = {
        "login": "your_awesome_courier_name_here",
        "password": "1234567"
        }

class TestBaseScooterOrder:
    BASE_SCOOTER_ORDER = {
        "firstName": "John",
        "lastName": "Dow",
        "address": "New York, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2024-06-06",
        "comment": "Here we go again",
        "color": [
            "BLACK"
        ]
        }