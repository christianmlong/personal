
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Jenv (Java Environment) setup
if which jenv &> /dev/null; then
    export JENV_ROOT=/usr/local/var/jenv
    eval "$(jenv init -)"
fi

# Oracle Instant Client setup
ORACLE_HOME=$HOME/.local/bin/oracle/instantclient_11_2
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$ORACLE_HOME
export PATH=$PATH:$ORACLE_HOME
export TNS_ADMIN=$ORACLE_HOME/network/admin
# export TNS_ADMIN=$ORACLE_HOME
