from playwright.sync_api import Page
from utils import websites_to_scap
from playwright._impl._errors import TimeoutError, Error


class BasePage():
    def __init__(self, page):
        super().__init__()
        self.page: Page = page

    def navigate(self, url):
        self.page.goto(url)

    def wait_for_page_to_load(self, timeout: float = 1000):
        self.page.wait_for_timeout(timeout)

    def scroll_down_page(self, count: int = 1):
        if isinstance(count, int):
            for i in range(count):
                self.page.keyboard.down('End')
        else:
            raise TypeError


class NieoznakowanyPage(BasePage):
    BUTTON_CLEAR_TABLE = "//button[@class='btn btn-outline-danger video-btn']"

    def click_clear_table_button(self):
        pass


class FacebookBasePage(BasePage):
    BASE_URL = websites_to_scap.Website.FACEBOOK.base_url

    def __init__(self, page):
        super().__init__(page)

    def close_login_info_modal(self):
        self.page.get_by_label("Zamknij").click()

    def close_allow_all_files_modal(self):
        self.page.get_by_role("button", name="Zezwól na wszystkie pliki").click()

    def remove_login_bottom_div(self):
        self.page.evaluate(
            '''document.evaluate('//a[@aria-label="Utwórz nowe konto"]/../../../../../../div', document, null, XPathResult.ANY_TYPE, null).iterateNext().remove()''')


class FacebookGroupPage(FacebookBasePage):
    def __init__(self, page, group_name):
        super().__init__(page)
        self.group_name = group_name
        self.navigate(f'{self.BASE_URL}/{self.group_name}/')

    def navigate_to_albums(self):
        self.page.goto(f'{self.BASE_URL}/{self.group_name}/photos_albums')
        return FacebookAlbumsPage(self.page)


class FacebookAlbumsPage(FacebookBasePage):
    def get_album_names(self) -> list:
        albums = []
        for album in self.page.locator(
                '//a[@role="link"]//span[contains(text(), "")]/../../../../../parent::a').element_handles():
            album_name = album.inner_text().splitlines()[0]
            photo_number = album.inner_text().splitlines()[1]
            albums.append((album_name, photo_number))
        return albums

    def open_album_details(self, album_name: str):
        self.page.locator(f'//span[contains(text(), "{album_name}")]').click(timeout=3000)
        self.wait_for_page_to_load(4000)
        return FacebookAlbumDetailsPage(self.page)


class FacebookAlbumDetailsPage(FacebookBasePage):
    def open_first_photo_in_album(self):
        try:
            self.page.locator('a[aria-label="Zdjęcie w albumie"]').element_handles()[0].click()
        except IndexError:
            self.page.locator('//div[@aria-label="Edytuj"]/../parent::a/parent::div').element_handles()[0].click()
        return FacebookPhotoDetailsPage(self.page)


class FacebookPhotoDetailsPage(FacebookBasePage):
    IMAGE_LOCATOR = '//div[@aria-label="Przeglądarka zdjęć"]//img[@data-visualcompletion="media-vc-image"]'
    ALT_IMAGE_LOCATOR = '//img[@data-visualcompletion="media-vc-image"]'

    def hover_over_photo(self):
        print('DEBUG', self.page.url)
        try:
            self.page.get_by_role("img", name="Brak dostępnego opisu zdjęcia.").hover(timeout=1000)
        except (TimeoutError, Error):
            try:
                self.page.locator(self.IMAGE_LOCATOR).hover(timeout=1000)
            except TimeoutError:
                self.page.locator(self.ALT_IMAGE_LOCATOR).hover(timeout=1000)

    def next_photo_button_is_visible(self):
        self.hover_over_photo()
        return self.page.get_by_label("Następne zdjęcie").is_visible()

    def show_more_button_is_visible(self):
        return self.page.get_by_role("button", name="Wyświetl więcej").is_visible()

    def click_first_show_more_button(self):
        self.page.get_by_role("button", name="Wyświetl więcej").element_handles()[0].click()

    def get_photo_description(self):
        return self.page.locator('//a[contains(@href, "hashtag")]/../parent::span[@dir="auto"]').inner_text(
            timeout=2000)

    def get_image_url(self):
        img_url = self.page.locator(self.IMAGE_LOCATOR).element_handles()[0].get_attribute('src')
        return img_url

    def click_next_picture(self, timeout: float = 3000):
        self.hover_over_photo()
        self.page.get_by_label("Następne zdjęcie").click(timeout=timeout)
