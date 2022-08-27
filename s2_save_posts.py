from json import loads, dumps
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from libs import login, timestamps as tst, scraping_tools as tools

driver = login.driver


with open('./temp/data.json', 'r') as r:
    data_to_process = loads(r.read())

processed = set(data_to_process.get('followed_posts') or [])
try:
    for k, (media_pk, post_code) in enumerate(data_to_process['posts_to_save_and_follow'].items(), 1):
        if media_pk in processed:
            continue
        print(
            tst.now('Europe/Moscow').strftime('%H:%M:%S'), 'saving post', f"https://www.instagram.com/p/{post_code}",
            f"({k}/{len(data_to_process['posts_to_save_and_follow'])})", '...',
        )
        sleep(tools.random_delay())

        driver.get(f"https://www.instagram.com/p/{post_code}")

        try:
            save_button = tools.load_then_do(
                lambda: driver.find_element(By.CSS_SELECTOR, 'span._aamz > div > div > button'),
                NoSuchElementException, print_not_found=False,
            )
        except NoSuchElementException:
            sorry = driver.find_elements(By.CSS_SELECTOR, 'section > main > div > div > div > h2')
            if len(sorry) == 1 and sorry[0].text == "Sorry, this page isn't available.":
                processed.add(media_pk)
                print('-- post skipped as deleted')
                continue
            else:
                raise
        try:
            save_icon = driver.find_element(By.CSS_SELECTOR, 'span._aamz > div > div > button > div > svg > path')
            already_saved = True
        except NoSuchElementException:
            save_icon = driver.find_element(
                By.CSS_SELECTOR, 'span._aamz > div > div > button > div._abm0._abl_ > svg > polygon',
            )
            already_saved = False
        if not already_saved:
            tools.load_then_do(lambda: save_button.click(), NoSuchElementException)
            print('-- saved')
            already_saved = True

        follow_button = driver.find_elements(By.CSS_SELECTOR, 'div._aar0._ad95._aar1 > div._aar2 > button > div > div')
        if len(follow_button) == 1:
            follow_button = follow_button[0]
            if follow_button.text == 'Follow':
                tools.load_then_do(lambda: follow_button.click(), NoSuchElementException)
                print('-- followed its author')
        else:
            input('please do something')

        processed.add(media_pk)
except:
    raise
finally:
    data_to_process['followed_posts'] = list(processed)
    with open('./temp/data.json', 'w') as w:
        w.write(dumps(data_to_process))
    print('progress saved')

driver.close()
