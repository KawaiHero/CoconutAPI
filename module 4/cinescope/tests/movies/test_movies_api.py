import pytest
from cinescope.constants import admin_creds


class TestMovieAPI:

    def test_get_movies(self, common_user):
        response = common_user.api.movie_api.get_movies_info()
        response_data = response.json()

        assert "movies" in response_data, "Oтсутствует movies в ответе"
        assert "count" in response_data, "Oтсутствует количество фильмов в ответе"
        assert "page" in response_data, "отсутствует page в ответе"


    def test_post_movie(self, super_admin, test_movie):

        response = super_admin.api.movie_api.post_movie(test_movie)
        response_data = response.json()

        assert "id" in response_data, "Oтсутствует ID в ответе"
        assert "name" in response_data, "Oтсутствует Name в ответе"

    def test_post_movie_by_user(self, common_user, test_movie):

        response = common_user.api.movie_api.post_movie(test_movie, expected_status=403)
        response_data = response.json()

        assert "error" in response_data, "Oтсутствует error в ответе"
        assert "statusCode" in response_data, "Oтсутствует statusCode в ответе"

    def test_get_movie_by_id(self, super_admin, test_movie):

        response = super_admin.api.movie_api.post_movie(test_movie)
        movie_id = response.json()["id"]
        movie_response = super_admin.api.movie_api.get_movie_by_id(movie_id)
        movie_response_data = movie_response.json()
        assert "id" in movie_response_data, "Oтсутствует ID в ответе"
        assert "name" in movie_response_data, "Oтсутствует Name в ответе"
        assert movie_response_data["name"] == test_movie["name"], "name не совпадает"


    @pytest.mark.parametrize("genre_id", [1, 2, 3])
    def test_get_movie_by_genre(self, super_admin, genre_id):
        movie_response = super_admin.api.movie_api.get_movie_by_filter(f"genreId={genre_id}")
        movie_response_data = movie_response.json()
        filtred_list = movie_response_data["movies"]
        for fl in filtred_list:
            assert fl["genreId"] == genre_id, "wrong data"

    @pytest.mark.parametrize("location", ["MSK", "SPB"])
    def test_get_movie_by_location(self, super_admin, location):
        movie_response = super_admin.api.movie_api.get_movie_by_filter(f"locations={location}")
        movie_response_data = movie_response.json()
        filtred_list = movie_response_data["movies"]
        for fl in filtred_list:
            assert fl["location"] == location, "wrong data"

    @pytest.mark.parametrize("min_price,max_price", [(100,300),(300,600), (600,900)], ids=["lowcost", "Premium", "VIP"])
    def test_get_movie_by_price(self, super_admin, min_price, max_price):
        movie_response = super_admin.api.movie_api.get_movie_by_filter(f"minPrice={min_price}&maxPrice={max_price}")
        movie_response_data = movie_response.json()
        filtred_list = movie_response_data["movies"]
        for fl in filtred_list:
            assert min_price < fl["price"] < max_price, "wrong data"

    def test_delete_movie(self,super_admin, test_movie):

        response = super_admin.api.movie_api.post_movie(test_movie)
        movie_id = response.json()["id"]

        del_response = super_admin.api.movie_api.delete_movie(movie_id)
        assert response.json()["name"] == del_response.json()["name"], "name не совпадает"

    def test_patch_movie(self, super_admin, wrong_movie, test_movie):
        super_admin.api.auth_api.authenticate(admin_creds)
        response = super_admin.api.movie_api.post_movie(wrong_movie)
        response_data = response.json()
        movie_id = response.json()["id"]

        patch_response = super_admin.api.movie_api.patch_movie(movie_id, test_movie)
        patch_response_data = patch_response.json()
        assert response_data["name"] != patch_response_data["name"], "Название фильма не изменилось"

    def test_wrong_id(self, super_admin, movie_id = 99999):
        movie_response = super_admin.api.movie_api.get_movie_by_id(movie_id, expected_status=404)
        movie_response_data = movie_response.json()
        assert "message" in movie_response_data, "Oтсутствует message в ответе"
        assert "error" in movie_response_data, "Oтсутствует error в ответе"
        assert "statusCode" in movie_response_data, "Oтсутствует statusCode в ответе"

    def test_post_empty(self, super_admin):
        empty_movie = {}
        super_admin.api.auth_api.authenticate(admin_creds)
        response = super_admin.api.movie_api.post_movie(empty_movie, expected_status=400)
        response_data = response.json()

        assert "message" in response_data, "Oтсутствует message в ответе"
        assert "error" in response_data, "Oтсутствует error в ответе"
        assert "statusCode" in response_data, "Oтсутствует statusCode в ответе"

