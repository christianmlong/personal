# ~/.bashrc: executed by bash(1) for non-login shells.

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# From Unix & Linux Stack Exchange
# http://unix.stackexchange.com/questions/1288/preserve-bash-history-in-multiple-terminal-windows
export HISTCONTROL=ignoredups:erasedups  # no duplicate entries
export HISTSIZE=100000                   # big big history
export HISTFILESIZE=100000               # big big history
shopt -s histappend                      # append to history, don't overwrite it

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

export VISUAL=vi
export EDITOR=vi

# TMUX
if which tmux 2>&1 >/dev/null; then
    #if not inside a tmux session, and if no session is started, start a new tmux session. 
    # My .tmux.conf has a "new-session -A" line that will create-or-attach
    test -z "$TMUX" && tmux attach 
fi

# virtualenvwrapper setup
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/projects
source /usr/local/bin/virtualenvwrapper.sh
