
# I used Homebrew to install the GNU Utilities. Put them first in the PATH
export PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH"
export MANPATH="/usr/local/opt/coreutils/libexec/gnuman:/usr/local/opt/findutils/share/man:$MANPATH"

if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Jenv setup
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

# Homebrew path setup
export PATH="/usr/local/bin:$PATH"
export PATH="/usr/local/sbin:$PATH"

# Homebrew python setup
export PATH="/usr/local/opt/python@2/bin:$PATH"

# Pyenv setup

# Setting PATH for Python 3.7
# The original version is saved in .bash_profile.pysave
PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:${PATH}"
export PATH

# Silence the zsh message
export BASH_SILENCE_DEPRECATION_WARNING=1
