import pytest

from cinescope.api.api_manager import ApiManager
from cinescope.constants import test_cases
from cinescope.models.base_models import RegisterUserResponse
from cinescope.utils.payload_mutate import mutate_payload


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        response = api_manager.auth_api.register_user(user_data=test_user)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == test_user.email, "Email не совпадает"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user.email, "Email не совпадает"

    @pytest.mark.parametrize("case, field, value", test_cases)
    def test_register_with_invalid_data(self, api_manager: ApiManager , test_user, case, field, value):
        invalid_user = mutate_payload(test_user, field, value)
        response = api_manager.auth_api.register_user(user_data=invalid_user, expected_status=400)
        response_data = response.json()

        assert "message" in response_data, "Oтсутствует message в ответе"
        assert "error" in response_data, "Oтсутствует error в ответе"
        assert "statusCode" in response_data, "Oтсутствует statusCode в ответе"