# vi: nospell


## Vim cheatsheet

### Movement



### Insert Mode
- `Ctrl-T` indent
- `Ctrl-D` dedent


### Changes


### Indentation

From [this Stack Overflow question](http://stackoverflow.com/a/5212123/456550)

In the commands below, "re-indent" means "indent lines according to your [indentation settings][3]." [`shiftwidth`][4] is the primary variable that controls indentation.


**General Commands**

    >>   Indent line by shiftwidth spaces
    <<   De-indent line by shiftwidth spaces
    5>>  Indent 5 lines
    5==  Re-indent 5 lines

    >%   Increase indent of a braced or bracketed block (place cursor on brace first)
    =%   Reindent a braced or bracketed block (cursor on brace)
    <%   Decrease indent of a braced or bracketed block (cursor on brace)
    ]p   Paste text, aligning indentation with surroundings

    =i{  Re-indent the 'inner block', i.e. the contents of the block
    =a{  Re-indent 'a block', i.e. block and containing braces
    =2a{ Re-indent '2 blocks', i.e. this block and containing block

    >i{  Increase inner block indent
    <i{  Decrease inner block indent

You can replace `{` with `}` or `B`, e.g. `=iB` is a valid block indent command. Take a look at ["Indent a Code Block"][5] for a nice example to try these commands out on.

Also, remember that

    .    Repeat last command

, so indentation commands can be easily and conveniently repeated.


**Re-indenting complete files**

Another common situation is requiring indentation to be fixed throughout a source file:

    gg=G  Re-indent entire buffer

You can extend this idea to multiple files:

    " Re-indent all your c source code:
    :args *.c
    :argdo normal gg=G
    :wall


Or multiple buffers:

    " Re-indent all open buffers:
    :bufdo normal gg=G:wall


**In Visual Mode**

    Vjj> Visually mark and then indent 3 lines


**In insert mode**

These commands apply to the current line:

    CTRL-t   insert indent at start of line
    CTRL-d   remove indent at start of line
    0 CTRL-d remove all indentation from line


**Ex commands**

These are useful when you want to indent a specific range of lines, without moving your
cursor.

    :< and :> Given a range, apply indentation e.g.
    :4,8>   indent lines 4 to 8, inclusive


**Indenting using markers**

Another approach is via [markers][6]:

    ma     Mark top of block to indent as marker 'a'

...move cursor to end location

    >'a    Indent from marker 'a' to current location


**Variables that govern indentation**

You can set these in your [.vimrc file][7].

    set expandtab       "Use softtabstop spaces instead of tab characters for indentation
    set shiftwidth=4    "Indent by 4 spaces when using >>, <<, == etc.
    set softtabstop=4   "Indent by 4 spaces when pressing <TAB>

    set autoindent      "Keep indentation from previous line
    set smartindent     "Automatically inserts indentation in some cases
    set cindent         "Like smartindent, but stricter and more customisable


Vim has intelligent indentation based on filetype. Try adding this to your .vimrc:

    if has ("autocmd")
        " File type detection. Indent based on filetype. Recommended.
        filetype plugin indent on
    endif



**References**

 - [Indent a code block][8] 
 - [Shifting blocks visually][9]
 - [Indenting source code][10]
 - `:help =`


  [1]: http://vimdoc.sourceforge.net/
  [2]: http://vim.wikia.com
  [3]: http://vim.wikia.com/wiki/VimTip83
  [4]: http://vimdoc.sourceforge.net/htmldoc/options.html#%27shiftwidth%27
  [5]: http://vim.wikia.com/wiki/Indent_a_code_block
  [6]: http://www.marksanborn.net/software/using-markers-in-vim/
  [7]: http://vimdoc.sourceforge.net/htmldoc/starting.html#vimrc
  [8]: http://vim.wikia.com/wiki/Indent_a_code_block
  [9]: http://vim.wikia.com/wiki/VimTip224
  [10]: http://vim.wikia.com/wiki/VimTip83


### Misc

#### Reload .vimrc

```
:so %   - if it's currently being edited
:so $MYVIMRC     - if it's not curently beng edited
```

#### Modelines

Add this comment at the top of a file, to set vim options for just that file. For example
```
# vi: nospell
```

#### Settings

Add a ? mark after the setting name and it will show the value
```
:set expandtab?
```

Use the `:set` command.

 - `:set autoindent?` prints the option, and its value, if any. Vim _toggle options_ (booleans, options that are on/off), like `autoindent`, are prefixed with `no` to indicate that they're turned off, so the result of `:set autoindent` will be `autoindent` or `noautoindent`.
 - `:set autoindent` turns `autoindent` on.
  - this form turns toggle options _on_
  - for number or string options, this shows the value of the option, so `:set textwidth` will also print the value of the option. For number or string options, `:set option` is equivalent to `:set option?`.
 - `:set autoindent!` inverts the option. `autoindent` becomes `noautoindent`.
 - `:set optiont&` reverts `option` to its default value. 
 - Set number or string options with `:set option=value`.

