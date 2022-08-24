from json import loads
import applescript


def set_comment(file_path, comment_text):
    applescript.tell.app("Finder", f'set comment of (POSIX file "{file_path}" as alias) to "{comment_text}" as Unicode text')


with open('./temp/data.json', 'r') as r:
    data = loads(r.read()) or {}
for path, meta in data.items():
    text = f'post: "{meta["post_url"]}" author: "{meta["author_url"]}"'
    set_comment(path, text)
