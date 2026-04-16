from cinescope.utils.data_generator import DataGenerator


def test_db_requests(super_admin, db_helper_movie, created_test_movie):
    assert created_test_movie == db_helper_movie.get_movie_by_id(created_test_movie.id)


def test_movie_db(super_admin, db_helper_movie):
    movie = DataGenerator.generate_movie_data()
    #assert db_helper_movie.get_movie_by_id(movie["id"])
    db_helper_movie.create_test_movie(movie)
    assert db_helper_movie.get_movie_by_id(movie["id"])
    del_resp = super_admin.api.movie_api.delete_movie(movie["id"])
    assert del_resp.status_code == 200
