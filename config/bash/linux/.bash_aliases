alias l='ls -alF'
alias cdv='cdvirtualenv'
alias cdsp='cdsitepackages'
alias cdp='cdproject'
alias ..='cd ..'
alias ...='cd .. && cd ..'
alias o='less -R'
alias psw='ps -efww'
alias du='ncdu'
alias top='htop'
alias autoclean='sudo apt-get clean && sudo apt-get autoclean && sudo apt-get autoremove'
alias off='sudo shutdown -h now && exit'
alias reboot='sudo shutdown -r now && exit'
alias py3='/opt/python3.4/bin/python3.4'
alias pyvenv3='/opt/python3.4/bin/pyvenv-3.4'
alias irc='irssi -c freenode'
alias gitinfo='~/projects/personal/util/bash/git-info.sh'
alias copydot='~/projects/personal/util/python/copy_dot_files.py'
# View the dir stack
alias drs='dirs -v'
alias gitserve='git daemon --reuseaddr --base-path=. --export-all --verbose --enable=receive-pack'
alias rnet='sudo ifdown eth1 && sudo ifup eth1'
alias pipdev='pip install -r ~/.virtualenvs/dev_requirements.txt'

function make_change_dir
{
    mkdir -p $1
    cd $1
}
alias mcd='make_change_dir'

function new_blog_post
{
    ~/projects/public-personal/blog/scripts/new_post.sh "$1";
}
alias nbp='new_blog_post'

# Sync the environment of an existing shell
#
#  tmux already updates the environment according to
#  the update-environment settings in the config. However
#  for existing shells you need to sync from from tmux's view
#  of the world.
function tmux_sync_env
{
    ssh_auth_sock=`tmux showenv | grep "^SSH_AUTH_SOCK"`
    ssh_connection=`tmux showenv | grep "^SSH_CONNECTION"`
    export ${ssh_auth_sock}
    export "${ssh_connection}"
}
alias tse='tmux_sync_env'
