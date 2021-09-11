from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import sys
import tempfile
from urllib import request
import zipfile

DEFAULT = '~/.vim'
SUB = 'bundle'

plugins = [
    ('vim-surround',
        'https://github.com/tpope/vim-surround/archive/f51a26d3710629d031806305b6c8727189cd1935.zip'),
    ('vim-tmux-navigator',
        'https://github.com/christoomey/vim-tmux-navigator/archive/6c0b5d2faa49f2059331a4004b34a916c96abcb3.zip'),
    ('vim-syntastic',
        'https://github.com/vim-syntastic/syntastic/archive/dd226673063b189683b98133d7a2243c1316e71e.zip'),
    ('taglist',
        'https://github.com/yegappan/taglist/archive/v4.6.zip'),
    ('ctrlp',
        'https://github.com/kien/ctrlp.vim/archive/564176f01d7f3f7f8ab452ff4e1f5314de7b0981.zip'),
    ('linediff',
        'https://github.com/AndrewRadev/linediff.vim/archive/681a3bc2944059692c91c61fd5c6e01afba28e62.zip'),
    ('vim-repeat',
        'https://github.com/tpope/vim-repeat/archive/master.zip'),
    ('vim-airline',
        'https://github.com/vim-airline/vim-airline/archive/v0.11.zip'),
    ('vim-airline-themes',
        'https://github.com/vim-airline/vim-airline-themes/archive/master.zip'),
    ('vim-solidity',
        'https://github.com/ChristianChiarulli/vim-solidity.git'),
]

def get_pathogen(dst):
    url = 'https://tpo.pe/pathogen.vim'
    path = os.path.join(dst, 'pathogen.vim')

    resp = request.urlopen(url)
    with open(path, 'w') as outfile:
        outfile.write(resp.read().decode())

    print(f'Downloaded pathogen to {dst}')

def download_extract_zip(name, url, dst, downloaddir='.',
                         rmzip=True, rmexisting=True):
    resp = request.urlopen(url)

    zipfile_path = os.path.join(downloaddir, f'{name}.zip')
    with open(zipfile_path, 'wb') as outfile:
        outfile.write(resp.read())

    zf = zipfile.ZipFile(zipfile_path)
    dirname = zf.namelist()[0]

    zf.extractall(dst)

    dstpath = os.path.join(dst, name)
    if rmexisting:
        shutil.rmtree(dstpath, ignore_errors=True)

    try:
        os.rename(os.path.join(dst, dirname), dstpath)
    except Exception as e:
        print(e)
        raise

    print(f'Downloaded {name}')
    os.remove(zipfile_path)

def _star(f):
    def inner(*args):
        return f(*args[0])
    return inner

def download_plugins(dst):
    tmpdir = tempfile.mkdtemp()
    try:
        arg_iters = [(name, url, dst, tmpdir) for name, url in plugins]
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(_star(download_extract_zip), arg_iters)
    finally:
        shutil.rmtree(tmpdir)


def prepare_dst():
    if len(sys.argv) == 1:
        dst = DEFAULT
    elif len(sys.argv) == 2:
        dst = sys.argv[1]
    else:
        raise ValueError('Too many system arguments')

    dst = os.path.expanduser(dst)
    if not os.path.isdir(dst):
        raise OSError(f'destination `{dst}` does not exist')

    # pathogen file
    os.makedirs(os.path.join(dst, 'autoload'), exist_ok=True)

    # plugins
    os.makedirs(os.path.join(dst, SUB), exist_ok=True)
    return dst

if __name__ == '__main__':
    dst = prepare_dst()

    get_pathogen(os.path.join(dst, 'autoload'))
    download_plugins(os.path.join(dst, SUB))


