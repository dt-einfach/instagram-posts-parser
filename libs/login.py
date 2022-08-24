from json import dumps
from os.path import isfile
from time import sleep

from selenium import webdriver

from libs import lib
from libs.local_storage import LocalStorage

driver = webdriver.Chrome()
local = LocalStorage(driver)
driver.get("https://www.instagram.com/")
logged_in = False
if isfile('./temp/tokens.json'):
    lib.insert_tokens(driver, local)
    sleep(3)
    driver.get("https://www.instagram.com/")
    input('press Enter if you are logged in')
    logged_in = True

if not logged_in:
    print('please log in')
    input('press Enter after login')
    logged_in = True

with open('./temp/tokens.json', 'w') as w:
    w.write(dumps({
        'local': local.items(),
        'cookies': driver.get_cookies(),
    }))

# for i in range(2):
#     print('looking for "Not now" button...')
#     not_now = tools.load_then_do(
#         lambda: tools.get_not_now_button(driver), NoSuchElementException,
#         attempts=5, print_not_found=False, raise_not_found=False,
#     )
#     if not_now:
#         print('click "Not now"')
#         sleep(tools.random_delay())
#         not_now.click()
#     else:
#         print('no more "Not now" buttons')
#         break
