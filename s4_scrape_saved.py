from json import loads, dumps
from os import mkdir
from os.path import isdir, isfile
from pathlib import Path
from time import sleep

from instagrapi import Client
from selenium.common import NoSuchElementException

import config
from libs import login, timestamps as tst, scraping_tools as tools

driver = login.driver
cl = Client()
cl.login(config.login, config.password)

sleep(5)
driver.get(f"https://www.instagram.com/{config.inst_username}/saved")

input('please scroll down all saved posts')
"""
all_posts_button = tools.load_then_do(
    lambda: tools.get_all_posts_button(driver), NoSuchElementException, attempts=2,
    print_not_found=False, raise_not_found=False,
)
if all_posts_button is not None:
    all_posts_button.click()

posts_to_download = {}
posts_space = tools.load_then_do(lambda: tools.get_posts_space(driver), NoSuchElementException)
posts = tools.load_then_do(lambda: tools.get_saved_posts(posts_space), NoSuchElementException)
while True:
    sleep(tools.random_delay())
    _ = posts[-1].screenshot_as_png
    new_posts = tools.load_then_do(lambda: tools.get_saved_posts(posts_space), NoSuchElementException)
    if len(new_posts) > len(posts):
        posts = new_posts
    else:
        break
"""
posts_to_download = {}
posts_space = tools.load_then_do(lambda: tools.get_posts_space(driver), NoSuchElementException)
posts = tools.load_then_do(lambda: tools.get_saved_posts(posts_space), NoSuchElementException)

downloaded = {}
skipped = set()
if not isdir('./downloads'):
    mkdir('./downloads')
with open('./temp/data.json', 'r') as r:
    data_to_process = loads(r.read()) or {}
downloaded_earlier = {p: m['post_url'] for p, m in (data_to_process.get('downloaded_media') or {}).items()}
print('downloading saved posts...')
try:
    for k, post in enumerate(posts, 1):
        post_url = post.get_attribute('href')
        skip_it = False
        for _path, _post_url in downloaded_earlier.items():
            if _post_url == post_url:
                if isfile(_path):
                    print(
                        '--', tst.now('Europe/Moscow').strftime('%H:%M:%S'),
                        'skipping post', post_url, '- it has been downloaded earlier', f"({k}/{len(posts)})",
                    )
                    skip_it = True
                break
        if skip_it:
            continue
        print(
            '--', tst.now('Europe/Moscow').strftime('%H:%M:%S'),
            'downloading post', post_url, f"({k}/{len(posts)})", '...',
        )
        sleep(tools.random_delay())
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
except Exception as e:
    print('~~', tst.now('Europe/Moscow').strftime('%H:%M:%S'), 'Exception:', e)
finally:
    data_to_process['downloaded_media'] = downloaded
    data_to_process['skipped_to_download'] = list(skipped)
    with open('./temp/data.json', 'w') as w:
        w.write(dumps(data_to_process))
    driver.close()
