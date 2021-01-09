
# I used Homebrew to install the GNU Utilities. Put them first in the PATH
export PATH="/usr/local/opt/coreutils/libexec/gnubin:/usr/local/opt/findutils/libexec/gnubin:$PATH"
export MANPATH="/usr/local/opt/coreutils/libexec/gnuman:/usr/local/opt/findutils/share/man:$MANPATH"

if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Jenv setup
if which jenv &> /dev/null; then
    export JENV_ROOT=/usr/local/var/jenv
    eval "$(jenv init -)"
fi

# Homebrew path setup
export PATH="/usr/local/bin:$PATH"
export PATH="/usr/local/sbin:$PATH"

# Setting PATH for Python 3
export PATH=/usr/local/opt/python/libexec/bin:$PATH

# Silence the zsh message
export BASH_SILENCE_DEPRECATION_WARNING=1
