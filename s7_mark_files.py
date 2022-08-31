from json import loads
from os import mkdir
from os.path import isdir, join as path_join
import applescript


def set_comment(file_path, comment_text):
    applescript.tell.app("Finder", f'set comment of (POSIX file "{file_path}" as alias) to "{comment_text}" as Unicode text')


def mark_files(project_dir):
    temp_dir = path_join(project_dir, 'temp')
    if not isdir(temp_dir):
        mkdir(temp_dir)
    with open(path_join(temp_dir, 'data.json'), 'r') as r:
        data_to_process = loads(r.read()) or {}
    downloaded_media = data_to_process['downloaded_media']
    for path, meta in downloaded_media.items():
        text = f"post: {meta['post_url']}\nauthor: {meta['author_url']}"
        set_comment(path, text)
        with open(path + '.txt', 'w') as w:
            w.write(text)


if __name__ == '__main__':
    mark_files('/Volumes/Elements/inst_project')
