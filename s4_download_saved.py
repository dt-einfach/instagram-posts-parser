from json import loads, dumps, JSONDecodeError
from os import mkdir
from os.path import isdir
from pathlib import Path
from time import sleep

from instagrapi import Client
from selenium.common import NoSuchElementException

import config
from libs import login, timestamps as tst, scraping_tools as tools

driver = login.driver
cl = Client()
cl.login(config.login, config.password)

account_button = tools.load_then_do(lambda: tools.get_account_button(driver), NoSuchElementException)
account_button.click()
saves_button = tools.load_then_do(lambda: tools.get_saves_button(driver), NoSuchElementException)
saves_button.click()
sleep(5)
all_posts_button = tools.load_then_do(lambda: tools.get_all_posts_button(driver), NoSuchElementException)
all_posts_button.click()

posts_to_download = {}
posts_space = tools.load_then_do(lambda: tools.get_posts_space(driver), NoSuchElementException)
posts = tools.load_then_do(lambda: tools.get_saved_posts(posts_space), NoSuchElementException)
while True:
    _ = posts[-1].screenshot_as_png
    new_posts = tools.load_then_do(lambda: tools.get_saved_posts(posts_space), NoSuchElementException)
    if len(new_posts) > len(posts):
        posts = new_posts
    else:
        break
downloaded = {}
skipped = set()
if not isdir('./downloads'):
    mkdir('./downloads')
print('downloading saved posts...')
for k, post in enumerate(posts, 1):
    post_url = post.get_attribute('href')
    print('--', tst.now('Europe/Moscow').strftime('%H:%M:%S'), 'downloading post', post_url, '...')
    media_pk = cl.media_pk_from_url(post_url)
    media_description = cl.media_info(media_pk)
    media_type, author = media_description.media_type, media_description.user
    author_url = f"https://www.instagram.com/{author.username}/"
    report_dict = {'media_pk': media_pk, 'author_url': author_url, 'post_url': post_url}
    if media_type == 1:  # photo
        path = cl.photo_download(media_pk, Path('./downloads'))
        downloaded[str(path)] = report_dict
    elif media_type == 2:  # reels
        path = cl.clip_download(media_pk, Path('./downloads'))
        downloaded[str(path)] = report_dict
    elif media_type == 8:  # a few images
        paths = cl.album_download(media_pk, Path('./downloads'))
        for path in paths:
            downloaded[str(path)] = report_dict
    else:
        print('unexpected media type:', media_type, '- post', post_url)
        skipped.add(post_url)
        continue
    print('-- done')

with open('./temp/data.json', 'r') as r:
    data_to_process = loads(r.read()) or {}
data_to_process['downloaded_media'] = downloaded
data_to_process['skipped_to_download'] = list(skipped)
with open('./temp/data.json', 'w') as w:
    w.write(dumps(data_to_process))

driver.close()
