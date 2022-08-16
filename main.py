from json import dumps
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

import tools

driver = webdriver.Chrome()
driver.get("https://www.instagram.com/")

# LOGIN CREDENTIALS: ---------------------------------------------------------------------------------------------------

print('logging in...')
username, password = tools.load_then_do(lambda: tools.login(driver), NoSuchElementException)
username.clear()
password.clear()
sleep(tools.random_delay())
username.send_keys("blumau12@protonmail.com")
sleep(tools.random_delay())
password.send_keys("9090Opop!")
sleep(tools.random_delay())
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
# TODO: login confirmation
print('logged in successfully')

for i in range(2):
    print('looking for "Not now" button...')
    not_now = tools.load_then_do(
        lambda: tools.get_not_now_button(driver), NoSuchElementException,
        attempts=5, raise_not_found=False,
    )
    if not_now:
        print('click "Not now"')
        sleep(tools.random_delay())
        not_now.click()
    else:
        print('no more "Not now" buttons')
        break

print('looking for "Direct" button...')
direct_button = tools.load_then_do(lambda: tools.get_direct_button(driver), NoSuchElementException)
sleep(tools.random_delay())
print('click "Direct"')
direct_button.click()

print('looking for your PM...')
your_pm_button = tools.load_then_do(lambda: tools.get_your_pm_button(driver), NoSuchElementException)
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

for message in messages:
    # TODO: check whether it is a post
    post_image = message.find_elements(By.CSS_SELECTOR, 'img')[1]
    tools.load_then_do(lambda: post_image.click(), NoSuchElementException)
    save_button = driver.find_element(By.CSS_SELECTOR, 'section._aamu._aat0 > span._aamz > div > div > button')
    try:
        save_icon = driver.find_element(By.CSS_SELECTOR, 'span._aamz > div > div > button > div > svg > path')
        already_saved = True
    except NoSuchElementException:
        save_icon = driver.find_element(By.CSS_SELECTOR, 'span._aamz > div > div > button > div._abm0._abl_ > svg > polygon')
        already_saved = False
    if not already_saved:
        tools.load_then_do(lambda: save_button.click(), NoSuchElementException)
        already_saved = True

input()
