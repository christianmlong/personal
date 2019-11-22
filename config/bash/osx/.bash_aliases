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
alias gdd='git dd'
alias gddd='git ddd'
alias gu='git up'
alias ag="ag --color --color-match '35'"
alias shove_it='git diff-index --quiet HEAD -- &&  ~/projects/public-personal/utilities/git/git_megamerge.sh || echo "Commit changes first"'
alias pr_it='git diff-index --quiet HEAD -- && ( ~/projects/public-personal/utilities/git/git_checkout_base_feature_branch.sh && hub pull-request -o -b alpha && git co local_integration && gu && git branch -d "$GIT_FLOAT_BASE_BRANCH" ) || echo "Commit changes first"'
alias tag_it='git diff-index --quiet HEAD -- && ( git co alpha && bumpversion_tag_and_release && bumpversion micro && git float && git push origin alpha && git push --tags ) || echo "Commit changes first"'
alias ship_it='git diff-index --quiet HEAD -- && ( git push origin master && git push origin $(git describe --tags --abbrev=0):master ) || echo "Commit changes first"'
alias run_local_tests='py.test --duration=10 -m "not glacial_test and not really_slow_test" -n auto -r w --ds=ciam.web.settings.local_test'
alias find_recorded_at="git diff -U0 | grepdiff '      \"recorded_at\":' --output-matching=hunk"
alias stage_recorded_at="git diff -U0 | grepdiff '      \"recorded_at\":' --output-matching=hunk | git apply --cached --unidiff-zero"
alias pytest_cov="pytest --cov=ciam --cov-report term --cov-report html --cov-config /Users/chlong2/projects/ciam_tpsd/.coveragerc && open /tmp/htmlcov/index.html"
alias scrum_update="vi /Users/chlong2/tmp/scrum_update.md && /Users/chlong2/projects/utility/webex_teams/scrum_update/scrum_update.sh"
alias notify="osascript -e 'display notification \"Job complete\" with title \"iTerm\"'"
alias refresh_ciam_mirror="gu && git co alpha && git ff upstream/alpha && git push && git co master && git ff upstream/master && git push && git push --tags && git co alpha"

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

    # shellcheck disable=SC2230
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
#
# function use_postgres_94
# {
#     # pg_ctl -w -D /usr/local/var/postgres91/data stop -s -m fast
#     # brew unlink postgresql91 && brew link postgresql
#     pg_ctl -w -D /usr/local/var/postgres94/data -l /usr/local/var/postgres94/data/server.log start
# }

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

    if [[ "$1" = '--lax' ]]; then
        PYLINTRC="$PYLINTRC_DIR/.pylintrc_lax"
    else
        PYLINTRC="$PYLINTRC_DIR/.pylintrc"
    fi
    shift

    ARGS=(
        "--jobs=0"
        "--rcfile=$PYLINTRC"
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

function pyclean {
    find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
}

# Prepare a new CIAM release
function prepare_ciam_release
{
    if [[ -n $(git status -s) ]]; then
        echo "Operation cancelled. The repo contains uncommitted changes."
        return 1
    fi

    export GIT_FLOAT_BASE_BRANCH=alpha
    git co alpha
    bumpversion_tag_and_release
    git push
    git co master
    git ff alpha
    git push
    git co alpha
    git branch -d master
    bumpversion micro
    git push
    git float
}

# Deploy to CIAM servers using AWX
function _generic_ciam_deploy
{
    TOWER_CLI='/Users/chlong2/.virtualenvs/towercli/bin/tower-cli'
    SKIP_LDAP_TAG=0
    SKIP_DB_VIEWS_TAG=0

    if [ "$#" -eq 0 ]; then
        echo "Too few arguments"
        return
    elif [ "$#" -gt 2 ]; then
        echo "Too many arguments"
        return
    fi

    if [ "$1" = "dev" ]; then
        if [ "$#" -eq 1 ]; then
            # For now, use my disruptive Epic branch on dev-01 by default.
            # DEV_BRANCH_NAME='alpha'
            DEV_BRANCH_NAME='EPIC0010050-new-source-of-alerts'
        elif [ "$#" -eq 2 ]; then
            DEV_BRANCH_NAME="$2"
        fi
        TEMPLATE_ID=52
        EXTRA_VARS="--extra-vars='ciam_version=\"$DEV_BRANCH_NAME\"'"
        DEPLOY_DESC="Dev CIAM server"
    elif [ "$1" = "dev2" ]; then
        if [ "$#" -eq 1 ]; then
            DEV_BRANCH_NAME='alpha'
        elif [ "$#" -eq 2 ]; then
            DEV_BRANCH_NAME="$2"
        fi
        TEMPLATE_ID=58
        EXTRA_VARS="--extra-vars='ciam_version=\"$DEV_BRANCH_NAME\"'"
        DEPLOY_DESC="Dev 02 CIAM server"
    elif [ "$1" = "stage" ]; then
        if [ "$#" -eq 2 ]; then
            echo "Can not deploy a named branch to Stage"
            return
        fi
        TEMPLATE_ID=25
        EXTRA_VARS=''
        DEPLOY_DESC="Stage CIAM server"
    elif [ "$1" = "prod" ]; then
        if [ "$#" -eq 2 ]; then
            echo "Can not deploy a named branch to Production"
            return
        fi
        TEMPLATE_ID=56
        EXTRA_VARS="--extra-vars='ciam_verify_production_deploy=\"Yes\"'"
        DEPLOY_DESC="Production CIAM server"
    else
        echo "Invalid option $1"
        return
    fi

    args=(job launch -J "$TEMPLATE_ID" --no-input --monitor)

    if [ -n "$EXTRA_VARS" ]; then
        args+=( "$EXTRA_VARS" )
    fi

    if [ "$SKIP_LDAP_TAG" -eq 1 ]; then
        args+=( "--skip-tags=ldap" )
    fi

    if [ "$SKIP_DB_VIEWS_TAG" -eq 1 ]; then
        args+=( "--skip-tags=ciam_db_views" )
    fi

    echo "Starting deploy to $DEPLOY_DESC"
    echo "Tower CLI command"
    echo "$TOWER_CLI" "${args[@]}"
    if "$TOWER_CLI" "${args[@]}"; then
        /usr/bin/osascript -e "display notification \"$DEPLOY_DESC deploy complete\" with title \"iTerm\""
    else
        /usr/bin/osascript -e "display notification \"*** $DEPLOY_DESC DEPLOY FAILED ***\" with title \"iTerm\""
    fi

}
alias dev_ciam_deploy='_generic_ciam_deploy dev'
alias dev2_ciam_deploy='_generic_ciam_deploy dev2'
alias stage_ciam_deploy='_generic_ciam_deploy stage'
alias PROD_ciam_deploy='_generic_ciam_deploy prod'
