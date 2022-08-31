from random import random
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


js_scroll = """
window.scrollTo(0, document.body.scrollHeight);
var scrolldown = document.body.scrollHeight;
return scrolldown;
"""


def random_delay():
    """
    :return: random float from 3. to 25.
    """
    return 3 + random() * 22


def load_then_do(action, exceptions, attempts=8, print_not_found=True, raise_not_found=True):
    if not hasattr(exceptions, '__iter__'):
        exceptions = (exceptions, )
    for i in range(attempts):
        try:
            sleep(random_delay())
            return action()
        except exceptions as e:
            if print_not_found:
                print(f"~~ {exceptions}: {e}")
    if raise_not_found:
        raise NoSuchElementException(f"load_then_do: passed {attempts} attempts")
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


def get_your_pm_button(driver, pm_name):
    return driver.find_element(By.XPATH, f"//div[contains(text(), '{pm_name}')]")


def get_pm_space(driver):
    sel = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/' \
          'section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div'
    return driver.find_element(By.XPATH, sel)


def get_account_button(driver):
    sel = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section' \
          '/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span/img'
    return driver.find_element(By.XPATH, sel)


def get_saves_button(driver):
    sel = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section' \
          '/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/a[2]/div'
    return driver.find_element(By.XPATH, sel)


def get_all_posts_button(driver):
    sel = 'div > div > div._aavc'
    return driver.find_element(By.CSS_SELECTOR, sel)


def get_posts_space(driver):
    sel = 'article'
    spaces = driver.find_elements(By.CSS_SELECTOR, sel)
    assert len(spaces) == 1, f"get_posts_space: {len(spaces)} spaces found"
    return spaces[0]


def get_saved_posts(posts_space):
    sel = 'a'
    return posts_space.find_elements(By.CSS_SELECTOR, sel)


def get_follow_button(driver):
    sel = 'button > div > div'
    elements = driver.find_elements(By.CSS_SELECTOR, sel)
    if len(elements) != 1:
        raise Exception('Many follow buttons found')
    return elements[0]


def its_a_profile(driver):
    'header > section > div._aa_m > h2'
    profile_name = driver.find_elements(By.CSS_SELECTOR, 'header > section > div._aa_m > h2')
    if len(profile_name) != 1:
        return False
    profile_logo = driver.find_elements(By.CSS_SELECTOR, 'header > div > div > canvas')
    if len(profile_logo) != 1:
        return False
    posts_space = driver.find_elements(By.CSS_SELECTOR, 'main > div > div._ab8w._ab94._ab99._ab9f._ab9m._ab9o._abcm')
    if len(posts_space) != 1:
        return False
    return True
