
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Jenv (Java Environment) setup
if which jenv &> /dev/null; then
    export JENV_ROOT=/usr/local/var/jenv
    eval "$(jenv init -)"
fi

