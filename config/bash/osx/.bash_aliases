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
alias off='sudo shutdown -h now && exit'
alias reboot='sudo shutdown -r now && exit'
alias gitinfo='~/projects/personal/util/bash/git-info.sh'
# View the dir stack
alias drs='dirs -v'
alias gitserve='git daemon --reuseaddr --base-path=. --export-all --verbose --enable=receive-pack'

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

