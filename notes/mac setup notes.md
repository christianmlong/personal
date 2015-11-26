

### Mac Setup Notes

#### Keyboard

Download and install [Karabiner](https://pqrs.org/osx/karabiner/index.html.en) and [Seil](https://pqrs.org/osx/karabiner/seil.html.en).

Open "System Preferences > Keyboard > Modifier Keys..." and change caps lock configuration to "No Action".

In Seil, change the keycode of the capslock key to 59. That will make it act like the Left Control key, on all keyboards - external and built-in.


In Karabiner, set these six options

 - Don't remap an internal keyboard
 - Don't remap Apple's keyboards
 - Command_L to Option_L
 - Command_R to Option_R
 - Option_L to Command_L
 - Option_R to Command_R


#### Display

Set the big Dell monitor as the primary display. Open System Preferences > Displays > Arrangement. Drag the displays around to match their physical layout. Drag the white menu bar over to the big display. That sets the big display as primary.

If the application switcher bar (that shows when cmd-tab is pressed) shows up on the wrong display, then go to the display you want it to show up on, and hover over the dock to make it appear. That will bring the app switcher bar to that display.

#### Firefox

Install Firefox, and set up Sync to pull all the settings from my other account. Do not use Sync for syncing the TabMixPlus settings - it messed up my settings. Instead, export the TabmixPlus settings and check them in to version control.

#### Backup

Install Cisco network backup, according to [these instructions](http://iwe.cisco.com/web/view-post/post/-/posts?postId=351000074).

#### iTerm2

Install iTerm2. Set it to use the Solarized Dark theme. Set it to Paste from Clipboard on right click.

#### plist tweaks

#### hidden files

By default, the Finder does not show hidden files (files beginning with a dot).

To make Finder show hidden files

    defaults write com.apple.finder AppleShowAllFiles YES

To make the file open dialog show hidden files

    defaults write -g AppleShowAllFiles -bool true

However, I had a problem with some non-native mac software (Perforce Diff and Kdiff3). When I would open the Open File Dialog, I would see the hidden files, but I could not select them or interact with them at all. In the native Mac TextEdit, when I use the Open File Dialog, I can see and open the hidden files.

I also read something about the hidden files not working in Column View, but this is unrelated - I am having this problem in List View.

#### Pycharm and ideaVim

I export all my PyCharm settings to this file

    ~/projects/public-personal/config/pycharm/settings.jar

To re-enable key repeat when using ideaVim with PyCharm

    defaults write com.jetbrains.PyCharm ApplePressAndHoldEnabled -bool false

A reboot is required to get the change to be effective.

#### Diff and Merge

I tried to set up some diff and merge utilities. Here's what didn't work.

Kdiff3 installed using Homebrew
The File Open dialog shows hidden files (once I set the option with `defaults write`). However, I can not select the files (ones that start with a dot) in the File Open dialog. In contrast, in TextEdit, I can select the hidden files and open them. Maybe a `qt` problem? An older version of the Open File dialog?

Perforce Diff, installed from a dmg
Same problem as Kdiff3, can't open hidden files from the Open File dialog.

PyCharm Diff
Pycharm comes with a Diff viewer, that you can invoke using the command line

    /Applications/PyCharm.app/Contents/MacOS/pycharm diff /full/path/to/dir/1 /full/path/to/dir/2

It has a lot of problems. It can't operate on dirs without a full path - it won't find dirs in the current working directory. Also, when you make changes in the diff or merge view, it saves them to the file immediately, with no save step or undo. I did not find a way to split large hunks. Worst, when you open it, it seems to used a cached view instead of the real status of the file system, and clicking the refresh button does nothing. You have to go to the A and B sides, and click the little "..." button to open the dir from within PyCharm Diff iteself to get it to show the current status of the filesystem. Maddening!

---

My first impressions of Beyond Compare are good. It opened a directory comparison, and enabled fine-grained merging and editing. It has a command-line accessible interface, and it can integrate with git as the default difftool and mergetool.

#### Personal repository

    mkdir ~/projects
    cd ~/projects
    brew install git
    git clone git@github.com:christianmlong/personal.git public-personal

#### Github ssh key fingerprints


https://help.github.com/articles/what-are-github-s-ssh-key-fingerprints/

What are GitHub's SSH key fingerprints?

Public key fingerprints can be used to validate a connection to a remote server.

These are GitHub's public key fingerprints (in hexadecimal format):

    16:27:ac:a5:76:28:2d:36:63:1b:56:4d:eb:df:a6:48 (RSA)
    ad:1c:08:a4:40:e3:6f:9c:f5:66:26:5d:4b:33:5d:8c (DSA)

These are the SHA256 hashes shown in OpenSSH 6.8 and newer (in base64 format):

    SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8 (RSA)
    SHA256:br9IjFspm1vxR3iA35FWE+4VTyz1hYVLIE2t1/CeyWQ (DSA)

GitHub also uses SSHFP DNS records to securely publish our SSH key fingerprints. You can query for our SSHFP records using the command below:

    dig SSHFP github.com +nostats +nocomments +nocmd
    # ;github.com.            IN  SSHFP
    # github.com.     300 IN  SSHFP   2 1 7491973E5F8B39D5327CD4E08BC81B05F7710B49
    # github.com.     300 IN  SSHFP   1 1 BF6B6825D2977C511A475BBEFB88AAD54A92AC73

#### dotfiles

I manage my dotfiles as symlinks in to my personal github repository. For OS X, I have a setup script that makes the symlinks and the needed directories.

    . ~/projects/public-personal/config/bash/osx/setup.sh

Start a new terminal


Now pull all my vim plugins

    cd ~/.vim/bundle
    . ./git_clone_vim_plugins.sh

#### Vim

OS X ships with Vim 7.3. To install 7.4, do this.

    brew install vim --override-system-vi

Be sure to close out the existing terminal window, and start a new one. Another possibility is this:

    brew unlink vim && brew link vim

Again, start a new terminal window to see if it takes effect.

Reference [this Reddit thread](http://www.reddit.com/r/vim/comments/2ukp5j/starting_homebrew_version_of_vim/) for more info.

#### Git

On my Cisco-provided Mac, I set my global user name and email to match my Cisco Github Enterprise account. Then, in my personal repo, I override that so my email is my personal Gmail account.

#### GNU utilities

OS X is a BSD at heart, and it ships with bizarro BSD utilities. Here's how to replace them with the old familiar GNU utilities.

First, enable the "dupes" repository.

    brew tap homebrew/dupes

Now install the GNU coreutils

    brew install coreutils

That installs the coreutils prefixed with a 'g'. We can make some path changes to fix that. Type:

    brew info coreutils

It will suggest some exports, put them in .bashrc.

    PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH"
    MANPATH="/usr/local/opt/coreutils/libexec/gnuman:/usr/local/opt/findutils/share/man:$MANPATH"

Now, install the rest of the GNU utils you want

    brew install bash-completion
    brew install binutils
    brew install diffutils
    brew install ed --with-default-names
    brew install findutils --with-default-names
    brew install gawk
    brew install gnu-indent --with-default-names
    brew install gnu-sed --with-default-names
    brew install gnu-tar --with-default-names
    brew install gnu-which --with-default-names
    brew install gnutls
    brew install grep --with-default-names
    brew install gzip
    brew install less
    brew install rsync
    brew install tmux
    brew install unzip
    brew install watch
    brew install wdiff --with-gettext
    brew install wget



#### Other Homebrew

    brew install caskroom/cask/brew-cask

    brew install cloc
    brew install cowsay
    brew install dos2unix
    brew install gist
    brew install gnupg
    brew install htop-osx
    brew install hub --HEAD
    brew install jrnl
    brew install kdiff3
    brew install keybase
    brew install libxslt
    brew install mtr
    brew install ncdu
    brew install python
    brew install python3
    brew install reattach-to-user-namespace
    brew install rename
    brew install ruby
    brew install ssh-copy-id
    brew install stress
    brew install trash
    brew install tree

#### Install powerline fonts

I'm using vim powerline, and it needs a special font. I'm using a patched version of Inconsolata-g, at 13 points. Here is the [collection of patched powerline fonts](https://github.com/powerline/fonts). In iTerm2, the powerline arrows don't quite match up, so I use a different font, "13 point Meslo LG M Regular for Powerline", for the non-ASCII font.

#### Setup Gists for Github Enterprise

Login to Cisco Github Enterprise using the `cist` alias.

    cist --login

That will store an OAuth token at `~/.gist.httpstipgithub.cisco.com`

Now you can publish Gists like this

    cist my_markdown_file.md


### Python

    brew install python python3

    # Note: don't use --user, not ready for prime time
    pip install --upgrade requests
    pip install --upgrade requests[security]
    pip install --upgrade pip setuptools virtualenv virtualenvwrapper

####
