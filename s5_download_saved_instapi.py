from json import loads, dumps
from os import mkdir
from os.path import isdir, isfile
from pathlib import Path

from instagrapi import Client

import config
from libs import timestamps as tst

cl = Client()
cl.login(config.login, config.password)

downloads_dir = 'D:\\instagram_eliah'
downloaded = {}
skipped = set()
if not isdir(downloads_dir):
    mkdir(downloads_dir)
with open('./temp/data.json', 'r') as r:
    data_to_process = loads(r.read()) or {}
posts = data_to_process['posts_to_download']
downloaded_earlier = {m['post_url']: p for p, m in (data_to_process.get('downloaded_media') or {}).items()}
print('downloading saved posts...')
try:
    for k, post_url in enumerate(posts, 1):
        skip_it = False
        if post_url in downloaded_earlier and isfile(downloaded_earlier[post_url]):
            continue
        print(
            '--', tst.now('Europe/Moscow').strftime('%H:%M:%S'),
            'downloading post', post_url, f"({k}/{len(posts)})", '...',
        )
        # sleep(tools.random_delay())
        media_pk = cl.media_pk_from_url(post_url)
        media_description = cl.media_info(media_pk)
        media_type, author = media_description.media_type, media_description.user
        author_url = f"https://www.instagram.com/{author.username}/"
        report_dict = {'media_pk': media_pk, 'author_url': author_url, 'post_url': post_url}
        if media_type == 1:  # photo
            path = cl.photo_download(media_pk, Path(downloads_dir))
            downloaded[str(path)] = report_dict
        elif media_type == 2:  # reels
            path = cl.clip_download(media_pk, Path(downloads_dir))
            downloaded[str(path)] = report_dict
        elif media_type == 8:  # a few images
            paths = cl.album_download(media_pk, Path(downloads_dir))
            for path in paths:
                downloaded[str(path)] = report_dict
        else:
            print('unexpected media type:', media_type, '- post', post_url)
            skipped.add(post_url)
            continue
except Exception as e:
    print('~~', tst.now('Europe/Moscow').strftime('%H:%M:%S'), 'Exception:', e)
finally:
    data_to_process.setdefault('downloaded_media', {})
    data_to_process['downloaded_media'].update(downloaded)
    data_to_process.setdefault('skipped_to_download', [])
    data_to_process['skipped_to_download'] += list(skipped)
    with open('./temp/data.json', 'w') as w:
        w.write(dumps(data_to_process))
    print('progress saved')
