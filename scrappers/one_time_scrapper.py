import time

from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError, Error
from pom.pages import NieoznakowanyPage, FacebookBasePage, FacebookGroupPage, FacebookPhotoDetailsPage
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


def get_data_from_facebook_group_albums(group_name: str, excluded_albums: list):
    with (sync_playwright() as playwright):
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()

        # go to facebook group page, navigate to albums and close all popups/modals
        fb_page = FacebookGroupPage(page, group_name)
        fb_albums_page = fb_page.navigate_to_albums()
        fb_albums_page.close_allow_all_files_modal()
        fb_albums_page.close_login_info_modal()

        # scroll down page to load more albums, and wait for the albums to load (hard wait)
        fb_albums_page.scroll_down_page(3)
        fb_albums_page.wait_for_page_to_load(2000)

        # get all album names that are in facebook group
        albums_to_scrap = fb_albums_page.get_album_names()

        # exclude albums
        for album in reversed(albums_to_scrap):
            if album[0] in excluded_albums:
                albums_to_scrap.remove(album)

        for album, number_of_pic in albums_to_scrap:
            fb_albums_page.scroll_down_page(3)
            album_details_page = fb_albums_page.open_album_details(album)
            fb_albums_page.scroll_down_page(2)
            fb_albums_page.wait_for_page_to_load(1500)

            photo_details_page = album_details_page.open_first_photo_in_album()

            photo_details_page.wait_for_page_to_load()
            i = 0
            photo_details_page.remove_login_bottom_div()
            while True:
                try:
                    if photo_details_page.show_more_button_is_visible():
                        photo_details_page.click_first_show_more_button()
                        photo_details_page.wait_for_page_to_load(300)
                except (TimeoutError, Error, IndexError):
                    pass
                with open(f'test_data/group_photos/cars_{album}', 'a+') as f:
                    try:
                        photo_description = photo_details_page.get_photo_description()
                    except TimeoutError:
                        photo_description = 'NO_PHOTO_DESCRIPTION'
                    try:
                        img_url = photo_details_page.get_image_url()
                    except:
                        img_url = 'NO_URL'
                    f.write(f'''DESCRIPTION: {photo_description} \nIMG_URL: {img_url} \n\n-------------\n\n''')
                i += 1
                print(f'{album} ({number_of_pic}) - {i}')
                try:
                    photo_details_page.wait_for_page_to_load()
                    photo_details_page.click_next_picture()
                except TimeoutError:
                    fb_page.navigate_to_albums()
                    fb_page.close_login_info_modal()
                    break
                page.wait_for_timeout(5000)
    context.close()


# get_data_from_nieoznakowany_pl()
get_data_from_facebook_group_albums('nieoznakowaneradiowozy', [])

# with (sync_playwright() as playwright):
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context(record_video_dir="videos/")
#     page = context.new_page()
#
#     fb_page = FacebookGroupPage(page, 'nieoznakowaneradiowozy')
#     fb_albums_page = fb_page.navigate_to_albums()
#     fb_albums_page.close_allow_all_files_modal()
#     fb_albums_page.close_login_info_modal()
#
#     fb_albums_page.navigate('https://www.facebook.com/photo/?fbid=788047204640374&set=a.156461303690511')
#     fb_albums_page.close_allow_all_files_modal()
#     fb_albums_page.close_login_info_modal()
#     pd = FacebookPhotoDetailsPage(fb_albums_page.page)
#     try:
#         pd.click_next_picture()
#     except TimeoutError:
#         fb_page.navigate_to_albums()
#         fb_page.close_login_info_modal()
#
#     fb_albums_page.scroll_down_page(3)
#     album_details_page = fb_albums_page.open_album_details('Zdjęcia na osi czasu')
#     print(album_details_page.page.url)
#     fb_albums_page.scroll_down_page(2)
#
#     print('DEBUG')
#     pd.page.wait_for_timeout(5000)
#
