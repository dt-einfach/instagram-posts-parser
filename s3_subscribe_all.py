from json import loads, dumps
from time import sleep

from selenium.common import NoSuchElementException

from libs import login, timestamps as tst, scraping_tools as tools

driver = login.driver

with open('./temp/data.json', 'r') as r:
    data_to_process = loads(r.read())

skipped_urls = set()
for url in data_to_process['urls_to_subscribe']:
    print(
        tst.now('Europe/Moscow').strftime('%H:%M:%S'), 'checking url', url, '...',
    )
    sleep(tools.random_delay())
    driver.get('https://www.' + url)
    sleep(tools.random_delay() * 3)
    its_a_profile = tools.its_a_profile(driver)
    if not its_a_profile:
        print('-- url', url, 'considered as not a profile, so skipping it')
        skipped_urls.add(url)
        continue
    follow_button = tools.load_then_do(lambda: tools.get_follow_button(driver), NoSuchElementException)
    if follow_button.text == 'Follow':
        tools.load_then_do(lambda: follow_button.click(), NoSuchElementException)
        print('-- followed')
if skipped_urls:
    data_to_process['skipped_urls'] = list(skipped_urls)
    with open('./temp/data.json', 'w') as w:
        w.write(dumps(data_to_process))

driver.close()
