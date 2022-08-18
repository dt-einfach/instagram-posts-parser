from json import loads
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from libs import login, timestamps as tst, scraping_tools as tools

driver = login.driver


with open('./temp/data.json', 'r') as r:
    data_to_process = loads(r.read())

for media_pk, post_code in data_to_process['posts_to_save_and_follow'].items():
    print(
        tst.now('Europe/Moscow').strftime('%H:%M:%S'), 'saving post', f"https://www.instagram.com/p/{post_code}", '...',
    )
    sleep(tools.random_delay())

    driver.get(f"https://www.instagram.com/p/{post_code}")

    save_button = tools.load_then_do(
        lambda: driver.find_element(By.CSS_SELECTOR, 'span._aamz > div > div > button'),
        NoSuchElementException, print_not_found=False,
    )
    try:
        save_icon = driver.find_element(By.CSS_SELECTOR, 'span._aamz > div > div > button > div > svg > path')
        already_saved = True
    except NoSuchElementException:
        save_icon = driver.find_element(
            By.CSS_SELECTOR, 'span._aamz > div > div > button > div._abm0._abl_ > svg > polygon',
        )
        already_saved = False
    if not already_saved:
        print('-- saved')
        tools.load_then_do(lambda: save_button.click(), NoSuchElementException)
        already_saved = True

    follow_button = driver.find_element(By.CSS_SELECTOR, 'div._aar0._ad95._aar1 > div._aar2 > button > div > div')
    if follow_button.text == 'Follow':
        print('-- followed its author')
        tools.load_then_do(lambda: follow_button.click(), NoSuchElementException)

driver.close()
