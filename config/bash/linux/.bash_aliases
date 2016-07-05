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
alias gl='clear && git lnp'
alias gll='git l'
alias gs='git st'
alias ga='git ap'
alias gc='git ci -m'


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
    if [ -n "$ssh_auth_sock" ]
    then
        export ${ssh_auth_sock}
    else
        echo "SSH_AUTH_SOCK is empty"
    fi

    ssh_connection=`tmux showenv | grep "^SSH_CONNECTION"`
    if [ -n "$ssh_connection" ]
    then
        export ${ssh_connection}
    else
        echo "SSH_CONNECTION is empty"
    fi
}
alias tse='tmux_sync_env'

# Set up a virtualenvironment with development tools
function pip_setup_dev_environment
{

    python -c 'import sys; print(sys.real_prefix)' 2>/dev/null && INVENV=1 || INVENV=0
    if [[ $INVENV -eq 0 ]]; then
        echo "Not in a virtual environment"
    else
        pip install --upgrade -r ~/.virtualenvs/dev_requirements.txt

        PYTEST_PATH=$VIRTUAL_ENV/bin/pytest
        # Remove the obsolete `pytest` script that pylint installs.
        if [[ -a $PYTEST_PATH ]]; then
            rm $PYTEST_PATH
            echo "Removed obsolete pytest script"
        else
            echo "Obsolete pytest script not found"
        fi
        echo $PYTEST_PATH
    fi

}
alias pipdev='pip_setup_dev_environment'

# Set up a new project with cookiecutter
function new_project_from_cookiecutter
{
    if [ "$1" -a "$2" ]; then
        echo Making virtualenv and cookiecutter project
        ENVNAME=$(python ~/projects/public-personal/python/cookiecutter/cookie.py "$1" "$2")
        echo $ENVNAME
        workon $ENVNAME
    else
        echo "Please give a project name and description"
    fi
}
alias cookie='new_project_from_cookiecutter'

function tree
{
    /usr/local/bin/tree -a
}
