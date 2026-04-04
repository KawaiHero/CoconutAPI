from cinescope.api.api_manager import ApiManager
from cinescope.constants import admin_creds


class TestMovieAPI:

    def test_get_movies_list(self, api_manager: ApiManager):

        response = api_manager.movie_api.get_movies_info()
        response_data = response.json()

        # Проверки
        assert "movies" in response_data, "Oтсутствует movies в ответе"
        assert "count" in response_data, "Oтсутствует количество фильмов в ответе"
        assert "page" in response_data, "отсутствует page в ответе"


    def test_post_movie(self, api_manager: ApiManager, test_movie):

        api_manager.auth_api.authenticate(admin_creds)
        response = api_manager.movie_api.post_movie(test_movie)
        response_data = response.json()

        assert "id" in response_data, "Oтсутствует ID в ответе"
        assert "name" in response_data, "Oтсутствует Name в ответе"

    def test_get_movie_by_id(self, api_manager: ApiManager, test_movie):
        api_manager.auth_api.authenticate(admin_creds)
        response = api_manager.movie_api.post_movie(test_movie)

        movie_id = response.json()["id"]
        movie_response = api_manager.movie_api.get_movie_by_id(movie_id)
        movie_response_data = movie_response.json()
        assert "id" in movie_response_data, "Oтсутствует ID в ответе"
        assert "name" in movie_response_data, "Oтсутствует Name в ответе"
        assert movie_response_data["name"] == test_movie["name"], "name не совпадает"

    def test_get_movie_by_genre(self, api_manager: ApiManager, genre_id = 3):

        movie_response = api_manager.movie_api.get_movie_by_genre(genre_id)
        movie_response_data = movie_response.json()
        filtred_list = movie_response_data["movies"]
        for fl in filtred_list:
            assert fl["genreId"] == genre_id, "wrong data"



    def test_delete_movie(self,api_manager: ApiManager, test_movie):
        api_manager.auth_api.authenticate(admin_creds)
        response = api_manager.movie_api.post_movie(test_movie)
        movie_id = response.json()["id"]

        del_response = api_manager.movie_api.delete_movie(movie_id)
        assert response.json()["name"] == del_response.json()["name"], "name не совпадает"

    def test_patch_movie(self, api_manager: ApiManager, test_movie):
        wrong_movie_data = {
            "name": "Movie naaame",
            "description": "Movie description",
            "price": 100,
            "location": "SPB",
            "imageUrl": "https://image.url",
            "published": True,
            "genreId": 1
}
        api_manager.auth_api.authenticate(admin_creds)
        response = api_manager.movie_api.post_movie(wrong_movie_data)
        response_data = response.json()
        movie_id = response.json()["id"]

        patch_response = api_manager.movie_api.patch_movie(movie_id, test_movie)
        patch_response_data = patch_response.json()
        assert response_data["name"] != patch_response_data["name"], "Название фильма не изменилось"

    def test_wrong_id(self, api_manager: ApiManager, movie_id = 99999):
        movie_response = api_manager.movie_api.get_movie_by_id(movie_id, expected_status=404)
        movie_response_data = movie_response.json()
        assert "message" in movie_response_data, "Oтсутствует message в ответе"
        assert "error" in movie_response_data, "Oтсутствует error в ответе"
        assert "statusCode" in movie_response_data, "Oтсутствует statusCode в ответе"

    def test_post_empty(self, api_manager: ApiManager):
        empty_movie = {}
        api_manager.auth_api.authenticate(admin_creds)
        response = api_manager.movie_api.post_movie(empty_movie, expected_status=400)
        response_data = response.json()

        assert "message" in response_data, "Oтсутствует message в ответе"
        assert "error" in response_data, "Oтсутствует error в ответе"
        assert "statusCode" in response_data, "Oтсутствует statusCode в ответе"