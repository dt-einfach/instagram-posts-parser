from json import loads, dumps
from os import mkdir
from os.path import isdir

from selenium.webdriver.common.by import By

import config
from libs import login

driver = login.driver

driver.get(f"https://www.instagram.com/{config.inst_username}/saved")

input('please scroll down all saved posts and turn off your internet connection')
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

print('downloading saved posts...')
# posts_space = tools.get_posts_space(driver)
posts_to_download = set()
old_posts = []
while True:
    posts = driver.find_elements(By.CSS_SELECTOR, 'div > div > a')
    if posts == old_posts:
        break
    k = 0
    for post in posts:
        href = post.get_attribute('href')
        if not href.startswith('https://www.instagram.com/p/'):
            continue
        if href not in posts_to_download:
            posts_to_download.add(href)
            k += 1
            if k == 10:
                break
    post.screenshot_as_png
    old_posts = posts.copy()

if not isdir('./temp'):
    mkdir('./temp')
with open('./temp/data.json', 'r') as r:
    data_to_process = loads(r.read()) or {}
data_to_process['posts_to_download'] = list(posts_to_download)
with open('./temp/data.json', 'w') as w:
    w.write(dumps(data_to_process))
print('progress saved')
print('success.')
driver.close()
