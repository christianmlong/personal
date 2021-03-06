# ~/.bashrc: executed by bash(1) for non-login shells.

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# From Unix & Linux Stack Exchange
# http://unix.stackexchange.com/questions/1288/preserve-bash-history-in-multiple-terminal-windows
export HISTCONTROL=ignoreboth:erasedups  # no duplicate entries, don't remember commands that start with space
export HISTSIZE=100000                   # big big history
export HISTFILESIZE=100000               # big big history
shopt -s histappend                      # append to history, don't overwrite it

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

PS1='\u@\h:\w\$ '
# enable color support of ls
test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# Bash Secrets
# Keep secret environment variables and oauth tokens out of version control.
# Instead, set them in .bash_secrets, and make sure to chmod 400 that file.
if [ -f ~/.bash_secrets ]; then
    . ~/.bash_secrets
fi


# Enable bash completion
if [ -f `brew --prefix`/etc/bash_completion ]; then
    . `brew --prefix`/etc/bash_completion
fi


export VISUAL=vi
export EDITOR=vi

# # TMUX
# if which tmux 2>&1 >/dev/null; then
#     #if not inside a tmux session, and if no session is started, start a new tmux session.
#     # My .tmux.conf has a "new-session -A" line that will create-or-attach
#     test -z "$TMUX" && tmux attach
# fi

# Enable bash completion for pandoc
# eval "$(pandoc --bash-completion)"

# Enable bash completion for my custom 'git float' and 'git mfloat' aliases
# Reference:
# http://stackoverflow.com/questions/11466991/git-aliases-command-line-autocompletion-of-branch-names
_git_float()
{
    _git_branch
}


# virtualenvwrapper setup

# This is using the brew-installed Python 3 to run the virtualenv automation.
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/projects
source /usr/local/bin/virtualenvwrapper.sh

# prettyprinter setup
# Enable prettyprinter formattting automatically in all python repl sessions.
# https://prettyprinter.readthedocs.io
export PYTHONSTARTUP=~/python_startup.py
