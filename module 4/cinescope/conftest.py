
from faker import Faker
import pytest
import requests

from cinescope.api.api_manager import ApiManager
from cinescope.constants import Roles
from cinescope.entities.user import User
from cinescope.resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator

faker = Faker()

@pytest.fixture(scope="session")
def test_user():

    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
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

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session):
    new_session = user_session()

    admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.ADMIN.value],
        new_session)

    admin.api.auth_api.authenticate(admin.creds)
    return admin