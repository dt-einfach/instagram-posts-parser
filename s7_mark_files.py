from json import loads
from os import mkdir, remove
from os.path import isdir, join as path_join, isfile
from exif import Image


def mark_files(project_dir):
    temp_dir = path_join(project_dir, 'temp')
    if not isdir(temp_dir):
        mkdir(temp_dir)
    with open(path_join(temp_dir, 'data.json'), 'r') as r:
        data_to_process = loads(r.read()) or {}
    downloaded_media = data_to_process['downloaded_media']
    total = len(downloaded_media)
    for k, (path, meta) in enumerate(downloaded_media.items(), 1):
        print('marking', k, 'of', total, '...')
        text = f"p: {meta['post_url']}\na: {meta['author_url']}"
        txt_path = path + '.txt'
        if path.endswith('.jpg'):
            try:
                with open(path, 'rb') as image_file:
                    my_image = Image(image_file)
                my_image.user_comment = text
                with open(path, 'wb') as new_image_file:
                    new_image_file.write(my_image.get_file())
            except Exception as e:
                print('~~', 'Error', e, 'for file', path)
        if not isfile(txt_path):
            with open(path + '.txt', 'w') as w:
                w.write(text)


if __name__ == '__main__':
    mark_files('C:\\Users\\David\\PycharmProjects\\instagram-posts-parser')
