" Convert Mardown to html and place on the clipboard.
" This isn't working, because of the pipe character.
" Vim thinks that it should interpret the pipe instead
" of passing it to bash.
" command! Pandoc execute "!pandoc % -t html -o - | pbcopy"
" command! Pandoc echom system("wc -c", "abcdefg")

" Preview markdown file in Marked
" nnoremap <leader>m :silent !open -a Marked\ 2.app '%:p'<cr>
nnoremap <leader>m :!open -a Marked\ 2.app '%:p'<cr><cr>

