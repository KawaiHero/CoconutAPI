
from faker import Faker
import pytest
import requests

from cinescope.api.api_manager import ApiManager
from utils.data_generator import DataGenerator

faker = Faker()

@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
     return ApiManager(session)

@pytest.fixture(scope="session")
def registered_user(api_manager: ApiManager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def test_movie():

    random_name = DataGenerator.generate_movie_name()
    random_description = DataGenerator.generate_movie_description()
    return {
        "name": random_name,
        "imageUrl": "https://image.url",
        "price": 100,
        "description": random_description,
        "location": "SPB",
        "published": True,
        "genreId": 1
}

@pytest.fixture(scope="session")
def wrong_movie():
    random_name = DataGenerator.generate_movie_name()
    random_description = DataGenerator.generate_movie_description()
    return {
        "name": f"Wrong {random_name}",
        "description": f"Wrong {random_description} ",
        "price": 100,
        "location": "SPB",
        "imageUrl": "https://image.url",
        "published": True,
        "genreId": 1
}
