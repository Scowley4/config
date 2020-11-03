#!/usr/bin/env python3
"""Common utils for config python scripts"""

import os
import sys
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


def ensure_moved(path, dst_dir):
    """Ensures that a file is moved to the destination directory"""
    try:
        os.rename(path, os.path.join(dst_dir, os.path.basename(path)))
    except OSError as e:
        pass


def link_exists(src, dst):
    """Returns true if the dst is a symlink to the src"""
    return (os.path.exists(dst) and
            os.path.islink(dst) and
            os.path.samefile(src, dst))


def ensure_link(src, dst, backupdir=None):
    """Ensures that the dst is a symlink to the src"""
    if link_exists(src, dst):
        print('Link exists', dst, 'to', src)
    else:
        print('Linking', dst)
        ensure_filedir(dst)
        if backupdir is None:
            ensure_removed(dst)
        else:
            print('Moving', dst, 'to', backupdir)
            ensure_moved(dst, backupdir)
        os.symlink(src, dst)


def clone(repo, path):
    """Clones a git repo to a give path relative to the home directory"""
    path = os.path.join(os.environ['HOME'], path)
    if not os.path.exists(path):
        ensure_filedir(path)
        os.system('git clone {} {}'.format(repo, path))


def link_dotfiles(config_path=None, files=None, include_git=False):
    """Create symlink for dotfiles in home directory"""
    backupdir = os.path.expanduser('~/.dotfilebackup')
    os.makedirs(backupdir, exist_ok=True)

    filenames = ['vimrc', 'vim', 'bashrc', 'tmux.conf',
                 'inputrc', 'ipython/profile_default/ipython_config.py',
                 'bash_profile']

    if include_git:
        filenames.append('gitconfig')

    home = os.environ['HOME']
    config_path = os.path.join(home, config_path) if config_path is not None else home
    dot_path = os.path.join(config_path, 'config', 'dotfiles')
    for filename in filenames:
        src = os.path.abspath(os.path.join(dot_path, filename))
        dst = os.path.join(home, '.'+filename)
        ensure_link(src, dst, backupdir)

if __name__=='__main__':
    link_dotfiles(include_git=('git' in sys.argv))
