" Save and run the current file in Python
nnoremap <leader>r :execute ':w' \| !python %<cr>

" Save and debug the current file in Python
nnoremap <leader>R :execute ':w' \| !python -m pdb %<cr>

" Save and run the current file in the iPython debugger
nnoremap <leader>i :execute ':w' \| !ipython -i %<cr>

" Save current file, then run py.test on just this file
nnoremap <leader>t :execute ':w' \| !py.test -rw -W ignore %<cr>

" Save current file, then run py.test. Drop in to debug mode on error.
nnoremap <leader>T :execute ':w' \| !py.test --pdb -x -rw -W ignore %<cr>

" Save current file, then run pylint on it
nnoremap <leader>l :execute ':w' \| !pylint --rcfile="/Users/chlong2/projects/public-personal/config/python/.pylintrc" %<cr>

" Save current file, then run pylint on it, using the pylint-django plugin
nnoremap <leader>d :execute ':w' \| !pylint --rcfile="/Users/chlong2/projects/public-personal/config/python/.pylintrc" --load-plugins pylint_django %<cr>

" " Save current file, then run it with Fabric
" nnoremap <leader>f :execute ':w' \| !fab %<cr>
