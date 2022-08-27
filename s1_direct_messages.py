from json import dumps
from os import mkdir
from os.path import isdir
from re import findall

from instagrapi import Client

import config

posts_to_save_and_follow = {}
urls_to_subscribe = set()


cl = Client()
cl.login(config.login, config.password)

print(f'downloading direct messages for user "{config.pm_name}"...')
threads = cl.direct_threads(amount=20, selected_filter="", thread_message_limit=1)
threads = [t for t in threads if t.thread_title == config.pm_name]
assert len(threads) == 1, f"Can't choose a thread from threads: {threads}"
thread = threads[0]
messages = cl.direct_messages(thread_id=int(thread.id), amount=50000)
for msg in messages:
    if msg.item_type == 'media_share':
        media = msg.media_share
        posts_to_save_and_follow[media.pk] = media.code
    elif msg.item_type == 'link':
        for url in findall(r'instagram.com\S+', msg.link['text']):
            urls_to_subscribe.add(url)
if not isdir('./temp'):
    mkdir('./temp')
with open('./temp/data.json', 'w') as w:
    w.write(dumps({
        'posts_to_save_and_follow': posts_to_save_and_follow,
        'urls_to_subscribe': list(urls_to_subscribe),
    }))
print('saved direct messages to file "temp/data.json"')
