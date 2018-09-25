#!/bin/bash

# This allows vim shell to use bash aliases e.g.
#
shopt -s expand_aliases

alias l='ls -alF --color=always'
alias ll='ls -alFrth --color=always'
alias cdv='cdvirtualenv'
alias cdsp='cdsitepackages'
alias cdp='cdproject'
alias ..='cd ..'
alias ...='cd ../..'
alias o='less -R'
alias psw='ps -efww'
alias du='ncdu'
alias off='sudo shutdown -h now && exit'
alias reboot='sudo shutdown -r now && exit'
alias gitinfo='~/projects/personal/util/bash/git-info.sh'
# View the dir stack
alias drs='dirs -v'
alias gitserve='git daemon --reuseaddr --base-path=. --export-all --verbose --enable=receive-pack'
alias ☁️='cowsay clooooud'
alias gzip='gzip -k'
alias gunzip='gunzip -k'
alias komodo='open -a "Komodo Edit 9"'
alias rm='trash'
alias rrm='/usr/local/opt/coreutils/libexec/gnubin/rm'
alias pyclean='find . -xdev -type f -name '"'*.pyc'"' -exec /usr/local/opt/coreutils/libexec/gnubin/rm {} +'
alias bumpversion_tag_and_release='cdproject && bumpversion release --tag && git push --tags'
alias gl='clear && git lnp'
alias gll='git l'
alias gs='git st'
alias ga='git ap'
alias gc='git ci -m'
alias gd='git d'
alias gdt='git dt'
alias gds='git ds'
alias gdts='git dts'
alias gu='git up'
alias ag="ag --color --color-match '35'"
alias shove_it='git diff-index --quiet HEAD -- &&  ~/projects/public-personal/utilities/git/git_megamerge.sh || echo "Commit changes first"'
alias pr_it='git diff-index --quiet HEAD -- && ( ~/projects/public-personal/utilities/git/git_checkout_feature_branch.sh && hub pull-request -o -b alpha ) || echo "Commit changes first"'
alias tag_it='git diff-index --quiet HEAD -- && ( git co alpha && bumpversion_tag_and_release && bumpversion micro && git float && git push origin alpha && git push --tags ) || echo "Commit changes first"'
alias ship_it='git diff-index --quiet HEAD -- && ( git push origin master && git push origin $(git describe --tags --abbrev=0):master ) || echo "Commit changes first"'
alias run_local_tests='py.test --duration=10 -m "not glacial_test and not really_slow_test" -n auto -r w --ds=ciam.web.settings.local_test'
alias find_recorded_at="git diff -U0 | grepdiff '      \"recorded_at\":' --output-matching=hunk"
alias stage_recorded_at="git diff -U0 | grepdiff '      \"recorded_at\":' --output-matching=hunk | git apply --cached --unidiff-zero"
alias pytest_cov="pytest --cov=ciam --cov-report term --cov-report html --cov-config /Users/chlong2/projects/next_ciam/.coveragerc && open /tmp/htmlcov/index.html"

function make_change_dir
{
    mkdir -p "$1"
    cd "$1" || exit
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
# No longer needed, as of Wednesday, July 18, 2018
# function remove_obsolete_pytest
# {
#     INVENV=$(in_virtualenv)
#     if [[ "$INVENV" -eq 0 ]]; then
#         echo "Not in a virtual environment"
#     else
#         PYTEST_PATH="$VIRTUAL_ENV/bin/pytest"
#         # Remove the obsolete `pytest` script that pylint installs.
#         if [[ -a "$PYTEST_PATH" ]]; then
#             rm "$PYTEST_PATH"
#             echo "Removed obsolete pytest script"
#         else
#             echo "Obsolete pytest script not found"
#         fi
#         echo "$PYTEST_PATH"
#     fi
# }

# Set up a virtualenvironment with development tools
function pip_setup_dev_environment
{
    INVENV=$(in_virtualenv)
    if [[ "$INVENV" -eq 0 ]]; then
        echo "Not in a virtual environment"
    else
        pip install --upgrade -r ~/.virtualenvs/dev_requirements.txt
        # remove_obsolete_pytest
    fi
}
alias pipdev='pip_setup_dev_environment'

# Set up a new project with cookiecutter
function new_project_from_cookiecutter
{
    if [ "$1" ] && [ "$2" ]; then
        echo Making virtualenv and cookiecutter project
        ENVNAME=$(python ~/projects/public-personal/python/cookiecutter/cookie.py "$1" "$2")
        echo "$ENVNAME"
        workon "$ENVNAME"
    else
        echo "Please give a project name and description"
    fi
}
alias cookie='new_project_from_cookiecutter'

# Publish gist to the SR&O Cisco Github Enterprise
function cisco_gist
{
    export GITHUB_URL='https://github4-chn.cisco.com/'
    gist "$@"
    unset GITHUB_URL
}
alias cist='cisco_gist'

# Publish gist to the company-wide Cisco Github Enterprise
function public_cisco_gist
{
    export GITHUB_URL='https://wwwin-github.cisco.com/'
    gist "$@"
    unset GITHUB_URL
}
alias pist='public_cisco_gist'

# Show the symlink, if any, with 'which'
function swhich
{
    # If the call to which succeeds, then show the alias if there is one.
    # More on capturing output, error, and return code from bash command
    # substitution:
    #    http://mywiki.wooledge.org/BashFAQ/002
    if THE_PATH=$(which "$1"); then
        ls -al "$THE_PATH"
    fi
}

# Activate and deactivate the different postgres versions I have installed
# function use_postgres_91
# {
#     pg_ctl -w -D /usr/local/var/postgres94/data stop -s -m fast
#     brew unlink postgresql && brew link postgresql91
#     pg_ctl -w -D /usr/local/var/postgres91/data -l /usr/local/var/postgres91/data/server.log start
# }

function use_postgres_94
{
    # pg_ctl -w -D /usr/local/var/postgres91/data stop -s -m fast
    # brew unlink postgresql91 && brew link postgresql
    pg_ctl -w -D /usr/local/var/postgres94/data -l /usr/local/var/postgres94/data/server.log start
}

function jrnl
{
    if [ -n "$TZ" ]; then
        export TZ_BACKUP_JRNL="$TZ"
        unset TZ
    fi
    /usr/local/bin/jrnl "$@"
    if [ -n "$TZ_BACKUP_JRNL" ]; then
        export TZ="$TZ_BACKUP_JRNL"
        unset TZ_BACKUP_JRNL
    fi
}

function alltree
{
    /usr/local/bin/tree -a "$@"
}

function analyze_csv
{
    PYTHON=$HOME/.virtualenvs/pandas_util/bin/python
    PROFILE_SCRIPT=$HOME/projects/cloned_apps/pandas-profiling/profile_csv.py

    if [ -f "$1" ]; then
        "$PYTHON" "$PROFILE_SCRIPT" --output "$1".html "$1"
    else
        echo 'Please specify a path to a CSV file'
    fi

}


# Scan with Pylint
function scan_with_pylint
{
    PYLINT_BIN="$VIRTUAL_ENV/bin/pylint"

    PYLINTRC_DIR="/Users/chlong2/projects/public-personal/config/python"

    PYLINT_MSG_FORMAT="'"'{path}:{line}:{column}: {symbol}: {msg}'"'"

    if [[ "$1" = '--lax' ]]; then
        PYLINTRC="$PYLINTRC_DIR/.pylintrc_lax"
    else
        PYLINTRC="$PYLINTRC_DIR/.pylintrc"
    fi
    shift

    ARGS=(
        "--jobs=0"
        "--rcfile=$PYLINTRC"
        "--msg-template=$PYLINT_MSG_FORMAT"
    )

    if [[ "$1" = '--django' ]]; then
        ARGS+=("--load-plugins=pylint_django")
    fi
    shift

    "$PYLINT_BIN" "${ARGS[@]}" "$@"
}
alias lint='scan_with_pylint --strict --no-django'
alias dlint='scan_with_pylint --strict --django'
alias lintlax='scan_with_pylint --lax --no-django'
alias dlintlax='scan_with_pylint --lax --django'

