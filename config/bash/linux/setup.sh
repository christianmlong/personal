#!/bin/bash

# Setup symlinks to dotfiles
ln -s ~/projects/public-personal/config/bash/linux/.bash_aliases ~/.bash_aliases
ln -s ~/projects/public-personal/config/bash/linux/.bashrc ~/.bashrc
ln -s ~/projects/public-personal/config/bash/linux/.dircolors ~/.dircolors
ln -s ~/projects/public-personal/config/git/.gitconfig ~/.gitconfig
ln -s ~/projects/public-personal/config/tmux/.tmux.conf ~/.tmux.conf
ln -s ~/projects/public-personal/config/vim/.vimrc ~/.vimrc
ln -s ~/projects/public-personal/config/vim/git_clone_vim_plugins.sh ~/.vim/bundle/git_clone_vim_plugins.sh
ln -s ~/projects/public-personal/config/vim/git_pull_all.sh ~/.vim/bundle/git_pull_all.sh
ln -s ~/projects/public-personal/config/virtualenv/postmkvirtualenv ~/.virtualenvs/postmkvirtualenv
ln -s ~/projects/public-personal/config/virtualenv/test_requirements.txt ~/.virtualenvs/test_requirements.txt

