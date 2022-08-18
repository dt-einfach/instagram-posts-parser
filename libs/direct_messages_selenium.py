from json import dumps
from os import mkdir
from os.path import isdir
from re import findall
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import config
from libs import login, scraping_tools as tools

driver = login.driver

print('looking for "Direct" button...')
direct_button = tools.load_then_do(lambda: tools.get_direct_button(driver), NoSuchElementException)
sleep(tools.random_delay())
print('click "Direct"')
direct_button.click()

print('looking for your PM...')
your_pm_button = tools.load_then_do(lambda: tools.get_your_pm_button(driver, config.pm_name), NoSuchElementException)
sleep(tools.random_delay())
print('click your PM')
your_pm_button.click()

print('scrolling PM up...')
pm_space = tools.load_then_do(lambda: tools.get_pm_space(driver), NoSuchElementException)

messages = tools.load_then_do(lambda: pm_space.find_elements(By.XPATH, './*'), NoSuchElementException)
while True:
    _ = messages[0].screenshot_as_png
    new_messages = tools.load_then_do(lambda: pm_space.find_elements(By.XPATH, './*'), NoSuchElementException)
    if len(new_messages) > len(messages):
        messages = new_messages
    else:
        break

urls_to_subscribe = set()
processed_messages = []
for message in messages:
    post_images = message.find_elements(By.CSS_SELECTOR, 'img')
    post_headings = messages[1].find_elements(By.CSS_SELECTOR, 'div > div._ab8w._ab94._ab97._ab9f._ab9k._ab9p._ab9z._aba9._abcm')
    if len(post_images) != 2 or len(post_headings) != 1:
        urls_to_subscribe.update(set(findall(r'instagram\.com/\S+', message.text)))
        continue
    post_image = post_images[1]
    tools.load_then_do(lambda: post_image.click(), NoSuchElementException)
    save_button = tools.load_then_do(
        lambda: driver.find_element(By.CSS_SELECTOR, 'section._aamu._aat0 > span._aamz > div > div > button'),
        NoSuchElementException,
    )
    try:
        save_icon = driver.find_element(By.CSS_SELECTOR, 'span._aamz > div > div > button > div > svg > path')
        already_saved = True
    except NoSuchElementException:
        save_icon = driver.find_element(By.CSS_SELECTOR, 'span._aamz > div > div > button > div._abm0._abl_ > svg > polygon')
        already_saved = False
    if not already_saved:
        tools.load_then_do(lambda: save_button.click(), NoSuchElementException)
        already_saved = True

    follow_button = driver.find_element(By.CSS_SELECTOR, 'div._aar0._ad95._aar1 > div._aar2 > button > div > div')
    if follow_button.text == 'Follow':
        tools.load_then_do(lambda: follow_button.click(), NoSuchElementException)

    close_button = driver.find_element(By.CSS_SELECTOR, 'div.rq0escxv.l9j0dhe7.du4w35lb > div > div.o9tjht9c.jar9mtx6.mbzxb4f5.njoytozt > div')
    tools.load_then_do(lambda: close_button.click(), NoSuchElementException)
    processed_messages.append(message)

if not isdir('./temp'):
    mkdir('./temp')
with open('./temp/urls_to_subscribe.json', 'w') as w:
    w.write(dumps(list(urls_to_subscribe)))
