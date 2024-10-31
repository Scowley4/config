Config
------

This repo contains configuration files for my personal setup, mostly for
centralizing and using my dotfiles (vim, bashrc, tmux).


------

Clone to home directory

```
cd config

python linkdots.py # Or python3
```

Get [pathogen](https://github.com/tpope/vim-pathogen)

```
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
```

Get [jedi-vim](https://github.com/davidhalter/jedi-vim)

```
git clone --recursive https://github.com/davidhalter/jedi-vim.git ~/.vim/bundle/jedi-vim
```
