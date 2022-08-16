from random import random
from time import sleep

from selenium.webdriver.common.by import By


js_scroll = """
window.scrollTo(0, document.body.scrollHeight);
var scrolldown = document.body.scrollHeight;
return scrolldown;
"""


def random_delay():
    """
    :return: random float from 1. to 3.
    """
    return 1 + random() * 2


def load_then_do(action, exceptions, attempts=32, raise_not_found=True):
    if not hasattr(exceptions, '__iter__'):
        exceptions = (exceptions, )
    for i in range(attempts):
        try:
            sleep(random_delay())
            return action()
        except exceptions:
            pass
    if raise_not_found:
        raise Exception(f"load_then_do: passed {attempts} attempts")
    else:
        return


def login(driver):
    username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    return username, password


def get_not_now_button(driver):
    return driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")


def get_direct_button(driver):
    return driver.find_element(By.CSS_SELECTOR, "a[href='/direct/inbox/']")


def get_your_pm_button(driver):
    return driver.find_element(By.XPATH, "//div[contains(text(), 'ho.brat')]")


def get_pm_space(driver):
    sel = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/' \
          'section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div'
    return driver.find_element(By.XPATH, sel)


def scroll_pm_up(driver):
    scrolldown = driver.execute_script(js_scroll)
    match = False
    while not match:
        last_count = scrolldown
        sleep(random_delay())
        scrolldown = driver.execute_script(js_scroll)
        if last_count == scrolldown:
            match = True
