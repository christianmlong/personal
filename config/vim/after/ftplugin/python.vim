" Runs after python.vim, to fix up its python file type behavior

" Keep vim from trying to do its auto-indent thing when I type a colon
" Reference
" http://stackoverflow.com/questions/19320747/prevent-vim-from-indenting-line-when-typing-a-colon-in-python
":setlocal indentkeys-=<:>

" Actually, I couldn't get this to work, there is a built-in vim python indent
" file that runs AFTER this after-ft file. Grrr.
"
" To diagnose, open a Python file for editing, and run :scriptfiles. That will
" show you all the vim scripts that have run, in order of precedence.
" Reference
" http://superuser.com/questions/166902/why-does-vim-ignore-files-in-vim-after-ftplugin
"
" When I did that, it showed me a built-in vim file at
" ~/projects/public-personal/config/vim/ftplugin/python.vim
" Sure enough, that was setting <:> as part of the indent keys.

" To fix it, I set an autocommand in .vimrc, and that really gets the last
" word.
" autocmd FileType python setlocal indentkeys-=<:>
