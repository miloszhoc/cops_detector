from playwright.sync_api import Page
from utils import websites_to_scap


class BasePage():
    def __init__(self, page):
        super().__init__()
        self.page: Page = page

    def navigate(self, url):
        self.page.goto(url)


class NieoznakowanyPage(BasePage):
    BUTTON_CLEAR_TABLE = "//button[@class='btn btn-outline-danger video-btn']"

    def click_clear_table_button(self):
        pass


class FacebookPage(BasePage):
    BASE_URL = websites_to_scap.Website.FACEBOOK.base_url

    def navigate_to_albums(self):
        self.page.goto(f'{self.BASE_URL}/nieoznakowaneradiowozy/photos_albums')
