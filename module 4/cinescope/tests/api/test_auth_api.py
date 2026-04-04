import pytest

from cinescope.api.api_manager import ApiManager

class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"


    @pytest.mark.parametrize("field",["email","fullName","password","passwordRepeat"])
    def test_register_without_required_fields(self, api_manager: ApiManager , test_user, field):
        invalid_user = test_user.copy()
        invalid_user.pop(field)
        response = api_manager.auth_api.register_user(invalid_user, expected_status=400)
        response_data = response.json()


        assert "message" in response_data, "Oтсутствует message в ответе"
        assert "error" in response_data, "Oтсутствует error в ответе"
        assert "statusCode" in response_data, "Oтсутствует statusCode в ответе"

    @pytest.mark.parametrize("email", [" ", "123", "mail@"])
    def test_register_with_invalid_email(self, api_manager: ApiManager, test_user, email):
        invalid_email = test_user.copy()
        invalid_email["email"] = email
        response = api_manager.auth_api.register_user(invalid_email, expected_status=400)
        response_data = response.json()

        assert "message" in response_data, "Oтсутствует message в ответе"
        assert "error" in response_data, "Oтсутствует error в ответе"
        assert "statusCode" in response_data, "Oтсутствует statusCode в ответе"