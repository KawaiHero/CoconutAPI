import time

import allure
import pytest
from playwright.sync_api import sync_playwright

from cinescope.ui_pages.login_page import CinescopLoginPage
from cinescope.ui_pages.movie_page import MoviePage
from cinescope.utils.data_generator import DataGenerator

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Movie")
@pytest.mark.ui
class TestMovie:
    @allure.title("Написание отзыва к фильму")
    def test_movie_review(self, registered_user):
        with sync_playwright() as playwright:
            review = DataGenerator.generate_movie_description()
            movie_id = '2450'


            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            login_page = CinescopLoginPage(page)

            login_page.open()
            login_page.login(registered_user.email, registered_user.password)



            movie_page = MoviePage(page)
            movie_page.assert_was_redirect_to_home_page()
            movie_page.pick_movie(movie_id)
            movie_page.assert_was_redirect_to_movie_page(movie_id)

            #movie_page.pick_value4()
            movie_page.send_review(review)

            time.sleep(5)
            browser.close()


