#!/usr/bin/env python3
"""Common utils for config python scripts"""

import os
import imp
from sys import argv
def ensure_filedir(filename):
    """Ensures that the directory path of a file exists"""
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError:
        pass


def ensure_removed(path):
    """Ensures that a file path is removed"""
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
    except OSError:
        pass


def link_exists(src, dst):
    """Returns true if the dst is a symlink to the src"""
    return (os.path.exists(dst) and
            os.path.islink(dst) and
            os.path.samefile(src, dst))


def ensure_link(src, dst):
    """Ensures that the dst is a symlink to the src"""
    if link_exists(src, dst):
        print('Link exists',dst,'to',src)
    else:
        print('Linking', dst)
        ensure_filedir(dst)
        ensure_removed(dst)
        os.symlink(src, dst)


def clone(repo, path):
    """Clones a git repo to a give path relative to the home directory"""
    path = os.path.join(os.environ['HOME'], path)
    if not os.path.exists(path):
        ensure_filedir(path)
        os.system('git clone {} {}'.format(repo, path))


def link_dotfiles(config_path=None):
    """Create symlink for dotfiles in home directory"""
    home = os.environ['HOME']
    config_path = os.path.join(home,config_path) if config_path else home
    dotfiles = os.path.join(config_path, 'config', 'dotfiles')
    for filename in ['vimrc', 'vim', 'bashrc', 'tmux.conf', 'gitconfig']:
        src = os.path.abspath(os.path.join(dotfiles, filename))
        dst = os.path.join(home, '.'+filename)
        ensure_link(src,dst)
if __name__=='__main__':
    if len(argv)>1: 
        link_dotfiles(argv[1])
    else:
        link_dotfiles()
