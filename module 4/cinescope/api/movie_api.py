from cinescope.custom_requester.custom_requester import CustomRequester
from cinescope.constants import MOVIE_URL


class MovieAPI(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIE_URL)

    def get_movies_info(self, expected_status=200):

        return self.send_request(
            method="GET",
            endpoint=f"movies",
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status = 200):
        return self.send_request(
            method="GET",
            endpoint=f"movies/{movie_id}",
            expected_status=expected_status
        )

    def get_movie_by_filter(self, filter, expected_status = 200):
        return self.send_request(
            method="GET",
            endpoint=f"movies?{filter}",
            expected_status=expected_status
        )

    def post_movie(self, movie_data, expected_status=201):

        return self.send_request(
            method="POST",
            endpoint=f"movies",
            data=movie_data,
            expected_status = expected_status

        )

    def delete_movie(self, movie_id, expected_status=200):

        return self.send_request(
            method="DELETE",
            endpoint=f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def patch_movie(self, movie_id, movie_data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"/movies/{movie_id}",
            data=movie_data,
            expected_status=expected_status
        )
