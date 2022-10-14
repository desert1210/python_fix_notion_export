import os
import re
from urllib.parse import unquote

def mdRead(filename:str) -> list:
    if os.path.isfile(filename) == False: return None
    with open(filename, mode='r', encoding='utf-8') as fh:
        text = fh.read()
        fh.close()
    return text.split('\n')

def mdWrite(filename:str, lines:list):
    with open(filename, 'w', encoding='UTF-8') as fh:
        fh.write('\n'.join(lines))
        fh.close()

def fixFilename(filename: str):
    rx = re.compile('^(.*)\s[A-Fa-f0-9]{32}\.md$')
    mt = rx.search(filename)
    return f'{mt.group(1)}.md'

def fixPage(oldroot:str):
    newroot = fixFilename(oldroot)
    directory = os.path.dirname(oldroot)
    md = mdRead(oldroot)
    rx = re.compile(r"\[(.*)\]\((.*)\)")
    for index, line in enumerate(md):
        mt = rx.search(line)
        if not mt is None:
            name = mt.group(1)
            old_name = os.path.join(directory, unquote(mt.group(2)))
            new_name = os.path.join(directory, f'{name}.md')
            if os.path.isfile(old_name):
                os.rename(old_name, new_name)
            md[index] = f'[{name}]({name}.md)'
    mdWrite(newroot, md)
    pass

if __name__ == '__main__':
    fixPage('sample/奇門遁甲金口直斷 fb257f7c84844df4b35a9451c7886dc5.md')