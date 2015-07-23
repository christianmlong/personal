# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Alias definitions.
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# Prompt, with full path
# Original
#export PS1='[\u@\h \W]\$'
# Ubuntu-style
#export PS1='\u@\h:\w\$ '
# Hybrid
export PS1='[\u@\h]\w\$ '
