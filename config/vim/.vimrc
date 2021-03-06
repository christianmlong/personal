" Pathogen
" This is a vim plugin manager
" All plugins found in ~/.vim/bundle will be automaticaly added to the
" 'runtimepath'
execute pathogen#infect()
syntax on
filetype plugin indent on
call pathogen#helptags()

" Import common settings
source ~/.vimrc_common

" Map jk to Esc so that you do not have to reach for the Esc button
inoremap jk <Esc>

" Settings for vim-sensible
set undodir^=~/.vim/undo

set encoding=utf-8

" Pretty colors
"set t_Co=256
" set background=dark
set background=light
" let g:solarized_contrast='high'
call togglebg#map("<F5>")
" I tried using the solarized theme just for Airline, and just using
" the more colorful default theme for vim itself. However, the reverse-
" highlighting in the default scheme did not work with the solarized
" color scheme in iterm. So, I went back to specifying solarized in vim
" as well.
colorscheme solarized

" Switch in and out of paste mode
set pastetoggle=<F10>

set relativenumber

" Allow hidden buffers
set hidden

" Remember more commands, search history, and undo levels
set history=1000
set undolevels=1000

" Disable some old unneeded features
set nocompatible
" set modelines=0

" viminfo
" https://stackoverflow.com/questions/23012391/how-and-where-is-my-viminfo-option-set/23036077
" https://vim.fandom.com/wiki/Copy,_cut_and_paste#Increasing_the_buffer_size
set viminfo='100,<50000,s1000,h
"           |    |      |     |
"           |    |      |     + disable search highlighting on startup
"           |    |      + don't save regisers larger than 1000kb
"           |    + keep 50,000 lines per register
"           + remember marks for last 100 files

" More fine-grained undo
inoremap <Space> <Space><C-g>u
inoremap <Return> <Return><C-g>u
" inoremap <Tab> <Tab><C-g>u
inoremap <BS> <BS><C-g>u
inoremap <Del> <Del><C-g>u
inoremap <c-u> <c-g>u<c-u>
inoremap <c-w> <c-g>u<c-w>

" From Steve Losh's vim guide
" http://stevelosh.com/blog/2010/09/coming-home-to-vim/
set ruler
set backspace=indent,eol,start
set laststatus=2

" Show tabs and trailing characters.
"set listchars=tab:»·,trail:·,eol:¬
set listchars=tab:»·,trail:·
set list

" Reformat paragraphs and list.
" nnoremap <Leader>r gq}

" Spaces instead of tabs
filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab

"Press F9 in normal mode or in insert mode to insert the current datestamp
nnoremap <F9> "=strftime("%Y-%m-%d %H:%M")<CR>P
inoremap <F9> <C-R>=strftime("%Y-%m-%d %H:%M")<CR>

" Make vim read .md files as Markdown
autocmd BufNewFile,BufReadPost *.md set filetype=markdown

" enable fenced code block syntax highlighting
" Reference https://github.com/tpope/vim-markdown
let g:markdown_fenced_languages = ['html', 'python', 'bash=sh']


function! FixWhiteSpace()
    " Save the cursor position for later
    let l = line(".")
    let c = col(".")
    " Remove trailing white space
    %s/\s\+$//e
    " Remove extra blank lines at eof
    " Note : In the replace pattern, you
    " have to use \r to represent newline
    " while in the search pattern, you use \n
    "            ¯\_(ツ)_/¯
    %s/\($\n\)\+\%$/\r/e
    " Restore the previous cursor position
    call cursor(l, c)
endfunction
nnoremap <silent> <Leader>ws :call FixWhiteSpace()<CR>
autocmd FileType python,javascript,text,sql,dosini,asciidoc autocmd FileWritePre    * :call FixWhiteSpace()
autocmd FileType python,javascript,text,sql,dosini,asciidoc autocmd FileAppendPre   * :call FixWhiteSpace()
autocmd FileType python,javascript,text,sql,dosini,asciidoc autocmd FilterWritePre  * :call FixWhiteSpace()
autocmd FileType python,javascript,text,sql,dosini,asciidoc autocmd BufWritePre     * :call FixWhiteSpace()

" Get the last word on fixing Python indentation so it doesn't indet
" spuriously on every darn colon.
autocmd FileType python setlocal indentkeys-=<:>
autocmd FileType python setlocal indentkeys-=:

" Enable spellcheck
set spelllang=en_us
set spellfile=~/.vim/spell/en.utf-8.add
autocmd BufRead,BufNewFile *.md setlocal spell
autocmd BufRead,BufNewFile *.txt setlocal spell
autocmd BufRead,BufNewFile *.rst setlocal spell
autocmd FileType gitcommit setlocal spell
" Word-completion from the spelling dictionary
" set complete+=kspell

" Only use one space after a period when wrapping text using J or gq
" http://stackoverflow.com/questions/4760428/how-can-i-make-vims-j-and-gq-commands-use-one-space-after-a-period
"
" Possible counterargument: Using two spaces makes it easier for vim to find
" the real end of a sentence that contains a sentence-like structure inside
" it. Set cpo+=J in .vimrc to tell vim you are using two spaces at the end of
" sentences.
" http://stevelosh.com/blog/2012/10/why-i-two-space/
:set nojoinspaces

" vim-airline config
let g:airline_powerline_fonts = 1
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = '|'

" " Ctrl-j/k deletes blank line below/above, and Alt-j/k inserts.
" nnoremap <silent><C-j> m`:silent +g/\m^\s*$/d<CR>``:noh<CR>
" nnoremap <silent><C-k> m`:silent -g/\m^\s*$/d<CR>``:noh<CR>
" nnoremap <silent><A-j> :set paste<CR>m`o<Esc>``:set nopaste<CR>
" nnoremap <silent><A-k> :set paste<CR>m`O<Esc>``:set nopaste<CR>

" " Tab Pages
" " Open multiple files, one file per tab:  vi -p *.py
" nnoremap tj :tabnext<CR>
" nnoremap tk :tabprev<CR>
" nnoremap tn :tabnew<CR>
" nnoremap td :tabclose<CR>

" Splits
" nnoremap <C-J> <C-W><C-J>
" nnoremap <C-K> <C-W><C-K>
" nnoremap <C-L> <C-W><C-L>
" nnoremap <C-H> <C-W><C-H>
set splitbelow
set splitright

" " Vim should ignore these files in its wildmenu
" " Also affects Ctrl-P.
" set wildignore+=/var/folders/gh/**,/private/var/folders/gh/**
set wildignore+=*.pyc

" Settings for Ctrl-P
"

" Use .gitignore as the source of what files to ignore.
let g:ctrlp_user_command = ['.git', 'cd %s && git ls-files -co --exclude-standard']
" Setup some default ignores
" let g:ctrlp_custom_ignore = {
"   \ 'dir':  '\v[\/](\.(git|hg|svn)|\_site)$',
"   \ 'file': '\v\.(exe|so|dll|class|png|jpg|jpeg)$',
" \}

" Use the nearest .git directory as the cwd
" This makes a lot of sense if you are working on a project that is in version
" control. It also supports works with .svn, .hg, .bzr.
let g:ctrlp_working_path_mode = 'r'

let g:ctrlp_max_history = 10000

" Use a leader instead of the actual named binding
nmap <leader>p :CtrlP<cr>

" Easy bindings for its various modes
nmap <leader>bb :CtrlPBuffer<cr>
nmap <leader>bm :CtrlPMRU<cr>

" Don't inlcude temp files in Ctrl-P MRU
" let g:ctrlp_mruf_exclude = '/tmp/.*\|/temp/.*'
let g:ctrlp_mruf_exclude = '/var/folders/*|/private/var/folders/*|/usr/local/share/vim/*'

" Open multiple files as hidden buffers
let g:ctrlp_open_multiple_files = 'i'

" Case-sensitive search for MRU files
" Not working currently 9/24/15
let g:ctrlp_mruf_case_sensitive = 1

" Set this to 1 to disable adding nonmodifiable buffers, for example help
" files, to the MRU list:
let g:ctrlp_mruf_exclude_nomod = 1

" Set this to 1 to set searching by filename (as opposed to full path) as the
" default
" Note: disabled on Tuesday, September 8, 2020. I was getting this error:
"
" E363: pattern uses more memory than 'maxmempattern'
" Error detected while processing function
" <SNR>81_PrtFocusMap[1]..<SNR>81_PrtAdd[4]..<SNR>81_BuildPrompt:
"
" Something to do with the regex, I think.
" let g:ctrlp_by_filename = 1

" " BufferGator
" " Use the right side of the screen
" let g:buffergator_viewport_split_policy = 'R'

" " I want my own keymappings...
" let g:buffergator_suppress_keymaps = 1

" " Go to the previous buffer open
" nmap <leader>j :BuffergatorMruCyclePrev<cr>

" " Go to the next buffer open
" nmap <leader>k :BuffergatorMruCycleNext<cr>

" " View the entire list of buffers open
" nmap <leader>bb :BuffergatorOpen<cr>

" " Close the buffergator pane
" nmap <leader>B :BuffergatorClose<cr>

" " To open a new empty buffer
" nmap <leader>T :enew<cr>

" " Close the current buffer and move to the previous one
" nmap <leader>bq :bp <BAR> bd #<cr>



" Gundo plugin
map <leader>u :GundoToggle<CR>
let g:gundo_prefer_python3 = 1

" Fugitive plugin
map <leader>g :Gstatus<CR>

" Trigger UltiSnips configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
" let g:UltiSnipsExpandTrigger="<tab>"
" let g:UltiSnipsJumpForwardTrigger="<tab>"
" let g:UltiSnipsJumpBackwardTrigger="<s-tab>"
" let g:UltiSnipsJumpForwardTrigger="<c-b>"
" let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" If you want :UltiSnipsEdit to split your window.
" let g:UltiSnipsEditSplit="vertical"







" From
" http://jeetworks.org/from-acolyte-to-adept-the-next-step-after-nop-ing-arrow-keys/
"
" Use relative number in insert mode, and absolute the rest of the time.
" set number
" if has('autocmd')
" augroup vimrc_linenumbering
"     autocmd!
"     autocmd WinLeave *
"                 \ if &number |
"                 \   set norelativenumber |
"                 \ endif
"     autocmd BufWinEnter *
"                 \ if &number |
"                 \   set relativenumber |
"                 \ endif
"     autocmd VimEnter *
"                 \ if &number |
"                 \   set relativenumber |
"                 \ endif
" augroup END
" endif

augroup vimrc_linenumbering
autocmd!
autocmd WinLeave *
\ if &number |
\ set norelativenumber |
\ endif
autocmd WinEnter *
\ if &number |
\ set relativenumber |
\ endif
augroup END

" Fix spelling errors quicker. Press Ctrl-L in insert mode to jump back to the
" nearest spelling error, fix it automatically, and return to the place I was
" editing.
inoremap <c-l> <c-g>u<Esc>[s1z=`]a<c-g>u

" " Use the system clipboard
" set clipboard=unnamed

" " Use the mouse for scrolling and for visual selection
" set mouse=a

" Use the mouse only for normal mode
" set mouse=n

" Note setting the mouse variable messes with tmux's mouse settings. So, I'll
" leave vim mouse off for now.

" This allows you to call aliases and bash functions with the :! command
" http://stackoverflow.com/questions/4642822/commands-executed-from-vim-are-not-recognizing-bash-command-aliases
" If you had a virtualenv activated when you started vim, then virtualenvwrapper throws an error at the start
" of the new interactive bash login. This also causes problems when piping a
" buffer through unix filters (:%!indent)
" set shellcmdflag=-ic

" Save and run the current file in Python
" Moved to .vim/ftplugin/python.vim
" nnoremap <leader>r :execute ':w' \| !python %<cr>

" Disable full-screen ex mode
nnoremap Q <nop>

" Shift-tab dedents
inoremap <S-Tab> <C-d>

" Easily close a buffer without closing the split
" http://stackoverflow.com/questions/4465095/vim-delete-buffer-without-losing-the-split-window
nnoremap <leader><C-d> :bp\|bd #<CR>

" Swap Ctrl-i and Ctrl-o
" Set Ctrl-o to be Forward and Ctrl-I to be Back
:nnoremap <C-I> <C-O>
:nnoremap <C-O> <C-I>

" Disable tab key in normal mode
"
" Note: There is no way to disable the tab key and still keep the behavior of
" Ctrl-I. Vim can not distinguish between Tab and Ctrl-I, because the terminal
" sends vim the same bytes for both actions.
" https://stackoverflow.com/questions/14641942/how-to-unmap-tab-and-do-not-make-ctrl-i-invalid-in-vim
" https://superuser.com/questions/770068/in-vim-how-can-i-remap-tab-without-also-remapping-ctrli
" https://groups.google.com/forum/#!topic/vim_use/DtAa014x0Z4
" https://groups.google.com/forum/#!topic/vim_dev/Ym6D-kWIsyo
" nnoremap <Tab> <nop>

" Show the commands as they are being typed.
" Something above is setting this to noshowcmd, but
" I'm not sure what. Anyway, set it to showcmd here
" at the end to override what is being set above.
set showcmd

" Use ag with ack.vim
if executable('ag')
  let g:ackprg = 'ag --vimgrep'
endif
cnoreabbrev ag Ack
nmap <leader>f :Ack -ws<space>
nmap <leader>F :Ack<space>

" Tell vim-rhubarb about enterprise github
let g:github_enterprise_urls = ['https://github4-chn.cisco.com', 'https://wwwin-github.cisco.com']

" Let vim shell use bash aliases.
" https://stackoverflow.com/questions/8841116/vim-not-recognizing-aliases-when-in-interactive-mode
let $BASH_ENV = "~/.bash_aliases"

" Use our own virtualenv for the Python Black code formatter
" let g:black_virtualenv = '/Users/chlong2/.virtualenvs/black'

" Interleave
" https://vi.stackexchange.com/questions/4575/merge-blocks-by-interleaving-lines
function! Interleave()
    " retrieve last selected area position and size
    let start = line(".")
    execute "normal! gvo\<esc>"
    let end = line(".")
    let [start, end] = sort([start, end], "n")
    let size = (end - start + 1) / 2
    " and interleave!
    for i in range(size - 1)
        execute (start + size + i). 'm' .(start + 2 * i)
    endfor
endfunction
