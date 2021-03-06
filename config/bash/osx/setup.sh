#!/bin/bash

# Install Vim Pathogen
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

# Setup symlinks to dotfiles
ln -s ~/projects/public-personal/config/bash/osx/.bash_aliases ~/.bash_aliases
ln -s ~/projects/public-personal/config/bash/osx/.bash_profile ~/.bash_profile
ln -s ~/projects/public-personal/config/bash/osx/.bashrc ~/.bashrc
# ln -s ~/projects/public-personal/config/bash/osx/dircolors.ansi-dark ~/.dircolors
ln -s ~/projects/public-personal/config/bash/osx/dircolors.ansi-light ~/.dircolors
ln -s ~/projects/public-personal/config/git/osx/.gitconfig ~/.gitconfig

ln -s ~/projects/public-personal/config/tmux/.tmux.conf ~/.tmux.conf
ln -s ~/projects/public-personal/config/vim/.vimrc ~/.vimrc
ln -s ~/projects/public-personal/config/vim/.ideavimrc ~/.ideavimrc
ln -s ~/projects/public-personal/config/vim/.vimrc_common ~/.vimrc_common

ln -s ~/projects/public-personal/config/vim/git_clone_vim_plugins.sh ~/.vim/bundle/git_clone_vim_plugins.sh
ln -s ~/projects/public-personal/config/vim/git_pull_all.sh ~/.vim/bundle/git_pull_all.sh

ln -s ~/projects/public-personal/config/vim/after ~/.vim/after
ln -s ~/projects/public-personal/config/vim/ftplugin ~/.vim/ftplugin
ln -s ~/projects/public-personal/config/vim/spell ~/.vim/spell

ln -s ~/projects/public-personal/config/readline/.inputrc .inputrc
ln -s ~/projects/public-personal/config/python/python_startup.py python_startup.py


mkdir -p ~/.virtualenvs
ln -s ~/projects/public-personal/config/virtualenv/postmkvirtualenv ~/.virtualenvs/postmkvirtualenv
ln -s ~/projects/public-personal/config/virtualenv/dev_requirements.txt ~/.virtualenvs/dev_requirements.txt

ln -s ~/projects/public-personal/config/python/.pdbrc.py ~/.pdbrc.py

mkdir -p ~/.config/yapf
ln -s ~/projects/public-personal/config/python/yapf ~/.config/yapf/style
