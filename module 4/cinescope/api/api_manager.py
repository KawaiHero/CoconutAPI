from cinescope.api.auth_api import AuthAPI
from cinescope.api.user_api import UserAPI

class ApiManager:

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
