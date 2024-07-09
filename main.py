import time

from playwright.sync_api import sync_playwright

from pom.pages import NieoznakowanyPage
from utils.voivodeships import Voivodeship
from utils.websites_to_scap import Website
from utils.utils import extract_data_from_urls


def get_data_from_nieoznakowany_pl():  # todo finish - save to db
    base_url = Website.NIEOZNAKOWANY.base_url
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        current_page = NieoznakowanyPage(page)

        urls = []
        for data in Voivodeship:
            print(f'checking {data.readable_name}')
            current_page.navigate(f'{base_url}/public/index.php?name=list&country={data.readable_name}&back=1')
            page.on('request', lambda request: urls.append(request.url) if 'change.php?' in request.url else '')
        car_data = extract_data_from_urls(urls)
        browser.close()


def get_data_from_facebook_group():
    with (sync_playwright() as playwright):
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{Website.FACEBOOK.base_url}/radiowozynieoznakowane/")
        page.get_by_role("button", name="Zezwól na wszystkie pliki").click()
        page.get_by_label("Zamknij").click()

        # for i in range(400):
        #     print(f'scrolling... ({i}/400)')
        #     page.keyboard.down('End')
        #     page.wait_for_timeout(600)
        # all_posts = page.locator('//div[@data-ad-comet-preview="message"]').element_handles()
        #
        # with open('cars_fb', 'w+') as f:
        #     for post in all_posts:
        #         f.write(f'{post.inner_text()} \n\n')


# get_data_from_nieoznakowany_pl()
get_data_from_facebook_group()
