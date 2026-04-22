from faker import Faker
import pytest
import requests

from cinescope.api.api_manager import ApiManager
from cinescope.constants import Roles, Location
from cinescope.db_requester.db_helpers import DBHelper, DBHelperMovie
from cinescope.entities.user import User
from cinescope.models.base_models import TestUser, RegisterUserResponse, TestMovie
from cinescope.resources.user_creds import SuperAdminCreds
from cinescope.utils.data_generator import DataGenerator
from sqlalchemy.orm import Session
from cinescope.db_requester.db_client import get_db_session
import pytest
from playwright.sync_api import sync_playwright

DEFAULT_UI_TIMEOUT = 30000


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()

faker = Faker()

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
     return ApiManager(session)

@pytest.fixture
def registered_user(api_manager: ApiManager, test_user):
    response = api_manager.auth_api.register_user(user_data=test_user)
    register_user_response = RegisterUserResponse(**response.json())

    assert register_user_response.email == test_user.email, "ID не совпадает"
    return test_user

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

@pytest.fixture(scope="function")
def test_movie_p() -> TestMovie:
    return TestMovie(
        name=DataGenerator.generate_movie_name(),
        imageUrl=faker.image_url(),
        price=faker.pyint(min_value=10, max_value=1000),
        description=DataGenerator.generate_movie_description(),
        location=Location.MSK.value,
        published=True,
        genreId=faker.pyint(min_value=1, max_value=10)
    )


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
    updated_data = test_user
    updated_data.verified = True
    updated_data.banned = False
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
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

@pytest.fixture(scope="module")
def db_session() -> Session:

    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:

    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def db_helper_movie(db_session) -> DBHelperMovie:

    db_helper_mov = DBHelperMovie(db_session)
    return db_helper_mov

@pytest.fixture(scope="function")
def created_test_user(db_helper):

    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def created_test_movie(db_helper_movie):

    movie = db_helper_movie.create_test_movie(DataGenerator.generate_movie_data())
    yield movie
    # Cleanup после теста
    if db_helper_movie.get_movie_by_id(movie.id):
        db_helper_movie.delete_movie(movie)