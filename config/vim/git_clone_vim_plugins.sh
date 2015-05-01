#!/bin/bash

set -u
set -e

git clone git://github.com/altercation/vim-colors-solarized
git clone git://github.com/tpope/vim-commentary
git clone git://github.com/tpope/vim-fugitive
git clone git://github.com/tpope/vim-repeat
git clone git://github.com/tpope/vim-sensible
git clone git://github.com/tpope/vim-surround
git clone git://github.com/tpope/vim-unimpaired

git clone git@github.com:bling/vim-airline.git
git clone git@github.com:kien/ctrlp.vim.git
# git clone git@github.com:jeetsukumaran/vim-buffergator.git

git clone git@github.com:bronson/vim-visual-star-search.git