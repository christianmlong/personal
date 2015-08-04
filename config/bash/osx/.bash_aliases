alias l='ls -alF'
alias cdv='cdvirtualenv'
alias cdsp='cdsitepackages'
alias cdp='cdproject'
alias ..='cd ..'
alias ...='cd .. && cd ..'
alias o='less -R'
alias psw='ps -efww'
alias du='ncdu'
alias top='sudo htop'
alias off='sudo shutdown -h now && exit'
alias reboot='sudo shutdown -r now && exit'
alias gitinfo='~/projects/personal/util/bash/git-info.sh'
# View the dir stack
alias drs='dirs -v'
alias gitserve='git daemon --reuseaddr --base-path=. --export-all --verbose --enable=receive-pack'
alias ☁️='cowsay clooooud'
alias gzip='gzip -k'
alias gunzip='gunzip -k'

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

# Are we in a virtual environment?  We can't return values from bash functions.
# Instead, in the calling function, use command substitution to get the result.
# For example:
#    MY_VAR=$(in_virtualenv)
function in_virtualenv
{
    python -c 'import sys; print(sys.real_prefix)' > /dev/null 2>&1 && INVENV=1 || INVENV=0
    echo "$INVENV"
}

# Remove obsolete "pytest" script, that comes with pylint
function remove_obsolete_pytest
{
    INVENV=$(in_virtualenv)
    if [[ $INVENV -eq 0 ]]; then
        echo "Not in a virtual environment"
    else
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

# Set up a virtualenvironment with development tools
function pip_setup_dev_environment
{
    INVENV=$(in_virtualenv)
    if [[ $INVENV -eq 0 ]]; then
        echo "Not in a virtual environment"
    else
        pip install --upgrade -r ~/.virtualenvs/dev_requirements.txt
        remove_obsolete_pytest
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

# Publish gist to Cisco Github Enterprise
function cisco_gist
{
    export GITHUB_URL='https://tip-github-1.cisco.com/'
    gist "$@"
    unset GITHUB_URL
}
alias cist='cisco_gist'

# Use hub to interact with Cisco Github Enterprise
function cisco_hub
{
    export GITHUB_HOST='tip-github-1.cisco.com'
    hub "$@"
    unset GITHUB_HOST
}
alias chub='cisco_hub'

# Show the symlink, if any, with 'which'
function swhich
{
    # If the call to which succeeds, then show the alias if there is one.
    # More on capturing output, error, and return code from bash command
    # substitution:
    #    http://mywiki.wooledge.org/BashFAQ/002
    if THE_PATH=$(which $1); then
        ls -al "$THE_PATH"
    fi
}

# Activate and deactivate the different postgres versions I have installed
function use_postgres_91
{
    pg_ctl -w -D /usr/local/var/postgres94/data stop -s -m fast
    brew unlink postgresql && brew link postgresql91
    pg_ctl -w -D /usr/local/var/postgres91/data -l /usr/local/var/postgres91/data/server.log start
}

function use_postgres_94
{
    pg_ctl -w -D /usr/local/var/postgres91/data stop -s -m fast
    brew unlink postgresql91 && brew link postgresql
    pg_ctl -w -D /usr/local/var/postgres94/data -l /usr/local/var/postgres94/data/server.log start
}

function jrnl
{
    if [ -n $TZ ]; then
        export TZ_BACKUP_JRNL=$TZ
        unset TZ
    fi
    /usr/local/bin/jrnl $@
    if [ -n $TZ_BACKUP_JRNL ]; then
        export TZ=$TZ_BACKUP_JRNL
        unset TZ_BACKUP_JRNL
    fi
}

function tree
{
    /usr/local/bin/tree -a
}

