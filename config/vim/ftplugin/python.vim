" Save and run the current file in Python
nnoremap <leader>r :execute ':w' \| !python %<cr>

" Save and run the current file in the iPython debugger
nnoremap <leader>i :execute ':w' \| !python -m ipdb %<cr>

" Save current file, then run py.test on just this file
nnoremap <leader>t :execute ':w' \| !py.test -rw -W ignore %<cr>

" Save current file, then run py.test in the current directory
" nnoremap <leader>T :execute ':w' \| !py.test -p no:django<cr>

" Save current file, then run pylint on it
nnoremap <leader>l :execute ':w' \| !pylint --rcfile="/Users/chlong2/projects/public-personal/config/python/.pylintrc" %<cr>

" Save current file, then run pylint on it, using the pylint-django plugin
nnoremap <leader>d :execute ':w' \| !pylint --rcfile="/Users/chlong2/projects/public-personal/config/python/.pylintrc" --load-plugins pylint_django %<cr>

" " Save current file, then run it with Fabric
" nnoremap <leader>f :execute ':w' \| !fab %<cr>
