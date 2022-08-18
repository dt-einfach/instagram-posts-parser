from json import loads
from os import mkdir
from os.path import isdir
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import libs.scraping_tools as tools


def insert_tokens(driver, local):
    if not isdir('./temp'):
        mkdir('./temp')
    with open('./temp/tokens.json', 'r') as r:
        tokens = loads(r.read())
    for cookie_dict in tokens['cookies']:
        driver.add_cookie(cookie_dict)
    for key, value in tokens['local'].items():
        local.set(key, value)


def auto_log_in(driver, real_login, real_password):
    print('logging in...')
    username, password = tools.load_then_do(lambda: tools.login(driver), NoSuchElementException)
    username.clear()
    password.clear()
    sleep(tools.random_delay())
    username.send_keys(real_login)
    sleep(tools.random_delay())
    password.send_keys(real_password)
    sleep(tools.random_delay())
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
