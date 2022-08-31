from json import loads, dumps
from os import mkdir
from os.path import isdir, join as path_join


def mark_files(project_dir, fake_downloads_dir, real_downloads_dir):
    temp_dir = path_join(project_dir, 'temp')
    if not isdir(temp_dir):
        mkdir(temp_dir)
    with open(path_join(temp_dir, 'data.json'), 'r') as r:
        data_to_process = loads(r.read()) or {}
    downloaded_media = data_to_process['downloaded_media']
    for path in list(downloaded_media):
        new_path = path.replace(fake_downloads_dir, real_downloads_dir)
        downloaded_media[new_path] = downloaded_media.pop(path)
    with open(path_join(temp_dir, 'data.json'), 'w') as w:
        w.write(dumps(data_to_process))
    print('progress saved')


if __name__ == '__main__':
    mark_files(
        'C:\\Users\\David\\PycharmProjects\\instagram-posts-parser',
        '/Elements/inst/',
        '/Volumes/Elements/inst/',
    )
