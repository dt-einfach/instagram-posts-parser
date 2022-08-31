from json import loads, dumps
from os import mkdir
from os.path import isdir, join as path_join
from time import sleep

from requests import get

from libs import timestamps as tst


def download(project_dir, downloads_dir, datalama_key):
    downloaded = {}
    skipped = set()
    temp_dir = path_join(project_dir, 'temp')
    if not isdir(downloads_dir):
        mkdir(downloads_dir)
    if not isdir(temp_dir):
        mkdir(temp_dir)
    with open(path_join(temp_dir, 'data.json'), 'r') as r:
        data_to_process = loads(r.read()) or {}
    posts = data_to_process['posts_to_download']
    downloaded_earlier = {
        m['post_url']: p
        for p, m in (data_to_process.get('downloaded_media') or {}).items()
    }
    skipped_earlier = data_to_process.get('skipped_to_download') or []
    print('downloading saved posts...')
    try:
        for k, post_url in enumerate(posts, 1):
            if post_url in downloaded_earlier:
                continue
            if post_url in skipped_earlier:
                continue
            print(
                '--', tst.now('Europe/Moscow').strftime('%H:%M:%S'),
                'downloading post', post_url, f"({k}/{len(posts)})", '...',
            )
            skip = False
            while True:
                try:
                    response = get(
                        'https://api.datalama.io/v1/media/by/url',
                        params={'url': post_url},
                        headers={'accept': 'application/json', 'x-access-key': datalama_key},
                    )
                    post = response.json()
                    if post.get('exc_type') == 'MediaNotFound':
                        skip = True
                        break
                    media_pk = post['pk']
                    break
                except KeyError as e:
                    print('--', 'KeyError', e)
                    sleep(5)
            if skip:
                skipped.add(post_url)
                continue
            author = post['user']
            media_type = post['media_type']
            author_url = f"https://www.instagram.com/{author['username']}/"
            report_dict = {'media_pk': media_pk, 'author_url': author_url, 'post_url': post_url}

            urls_paths = {}
            if media_type in (1, 2):  # image or reels
                resolution = None
                chosen_url = None
                for version in post[f"{'image' if media_type == 1 else 'video'}_versions"]:
                    new_resolution = version['width'] * version['height']
                    if resolution is None or new_resolution > resolution:
                        resolution = new_resolution
                        chosen_url = version['url']
                path = path_join(downloads_dir, f"{author['username']}_{post['pk']}." + ('jpg' if media_type == 1 else 'mp4'))
                urls_paths[chosen_url] = path
            elif media_type == 8:  # album
                for resource in post['resources']:  # media_type = 8
                    resolution = 0
                    chosen_url = None
                    for version in resource['image_versions']:
                        new_resolution = version['width'] * version['height']
                        if new_resolution > resolution:
                            resolution = new_resolution
                            chosen_url = version['url']
                    path = path_join(downloads_dir, f"{author['username']}_{resource['pk']}.jpg")
                    urls_paths[chosen_url] = path
            else:
                print('unexpected media type:', media_type, '- post', post_url)
                skipped.add(post_url)
                continue
            for url, path in urls_paths.items():
                file = get(url)
                with open(path, 'wb') as wb:
                    wb.write(file.content)
                downloaded[str(path)] = report_dict
    # except Exception as e:
    #     print('~~', tst.now('Europe/Moscow').strftime('%H:%M:%S'), 'Exception:', e)
    finally:
        data_to_process.setdefault('downloaded_media', {})
        data_to_process['downloaded_media'].update(downloaded)
        data_to_process.setdefault('skipped_to_download', [])
        data_to_process['skipped_to_download'] += list(skipped)
        with open(path_join(temp_dir, 'data.json'), 'w') as w:
            w.write(dumps(data_to_process))
        print('progress saved')


if __name__ == '__main__':
    import config_datalama as cfg
    try:
        download(cfg.project_folder, cfg.downloads_folder, cfg.datalama_key)
    except KeyboardInterrupt:
        pass
