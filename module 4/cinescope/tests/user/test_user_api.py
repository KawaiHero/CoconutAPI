from cinescope.api.api_manager import ApiManager
from cinescope.constants import admin_creds


class TestUserAPI:
    def test_delete_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию и последующее удаление пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()


        # Проверки
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

        user_id = response_data["id"]
        api_manager.auth_api.authenticate(admin_creds)

        api_manager.user_api.delete_user(user_id)

        api_manager.user_api.get_user_info(user_id)
