from enum import Enum

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
MOVIE_URL = 'https://api.dev-cinescope.coconutqa.ru/'
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"

admin_creds = ("api1@gmail.com","asdqwe123Q")

test_cases = [
    ("missing_fullName", "fullName", None),
    ("missing_email", "email", None),
    ("invalid_email_format", "email", "abc"),
    ("short_password", "password", "123"),
]

