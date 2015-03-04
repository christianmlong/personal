Title: Looking for a new editor
Category: Python
Tags: komodo pycharm editor
Date: 2014-12-19 10:35
Author: Christian Long
Summary: Need a new editor

I'm looking for a new code editor. I have been using [Komodo](http://komodoide.com/) for ten years, and it has been very solid. I'm on Komodo 4 now; I like the project tree, which makes it easy to organize live and static folders, and local and remote files. It offers simple incremental search, and a good, clean interface for global find and replace in all open files.

Unfortunately, later versions of Komodo have introduced some features I can't get used to. The Project pane was split in to Projects and Places, and it does not work well for managing big projects on remote servers. Also, the incremental search was changed for the worse.

I have been looking at [PyCharm](https://www.jetbrains.com/pycharm/). I like its code completion features, and I figured out how to do find and replace in just open files (when doing a find, choose a custom Scope, and choose Open Files). The multiple-cursor editing is better than in Komodo 9 beta: for example alt-click adds a new cursor to the current group. The refactoring support looks great. I'm not a big fan of the way remote files are handled. They are copied down to the local system, and then the editor syncs changes back to the remote system. Also, the backspace key eats up whole indents, not just one space character [(bug report)](https://youtrack.jetbrains.com/issue/IDEA-87318). If I wanted tab-like behavior, I'd use tabs!

One other possibility I'm looking at is using cygwin. A full tmux, vim, fish shell and powerline setup would be very nice.
