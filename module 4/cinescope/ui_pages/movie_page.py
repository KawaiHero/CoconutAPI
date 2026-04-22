import allure
from playwright.async_api import Page

from cinescope.ui_pages.base_page import BasePage

class MoviePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}movies"


        self.movie_review = 'textarea[name="text"]'
        self.send_button = 'button[type="submit"]'
        self.value_button = 'div[class="w-16"] button'
        self.value = 'div[class="w-16"] select option[value="4"]'
        self.review_label = 'div[class="mt-10 w-[500px]"] [class="text-3xl"]'

    @allure.step("Выбор фильма по ID")
    def pick_movie(self,movie_id: str):
        url = f'{self.url}/{movie_id}'
        self.open_url(url)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_was_redirect_to_movie_page(self, movie_id: str):
        url = f'{self.url}/{movie_id}'
        self.wait_redirect_for_url(url)

    def pick_value4(self):
        self.click_element(self.value_button)
        self.click_element(self.value)

    @allure.step("Заполнение и отправка отзыва: {review}")
    def send_review(self, review: str):
        self.enter_text_to_element(self.movie_review, review)
        self.click_element(self.send_button)
