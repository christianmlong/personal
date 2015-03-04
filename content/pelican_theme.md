Title: More on Pelican themes 
Category: Python
Tags: 
Author: Christian Long
Summary: Adding the pelican-themes project as a git submodule 

The [Pelican Themes](https://github.com/getpelican/pelican-themes) project gathers together a bunch of nice themes for the [Pelican](http://docs.getpelican.com) static blog generator. 

This is a good case for using git's [submodule](http://git-scm.com/book/en/v2/Git-Tools-Submodules) feature. 

Move to where your Pelican is installed (where your pelicanconf.py file is). 

    $ cd ~/personal/blog

Make sure you are in a git working copy and the status is clean.

    $ git status

Add the pelican-themes repository as a git submodule, and commit the change.

    $ git submodule add git@github.com:getpelican/pelican-themes.git themes
    $ git commit -am "Add pelican-themes as a submodule"

Now we should see the submodule listed

    $ git submodule status

The pelican-themes project is itself made up of git submodules. Let's take a look.
Change to the newly-created themes directory, and look at the submodules defined in there

    $ git submodule status

    -656296ab29a76d980155427f1f1ffe1892966a2a BT3-Flat
    -a74606061d62be0f8508ca840375abe52ae24786 Responsive-Pelican
    -bd337dffaa8aca10a1757d17385030e3a9d6b835 alchemy
    -4ea9f35b517e67488f330799e8637e2e045d657e blue-penguin
    . . . etc.

Here `git submodule status` prints all the submodules that make up the pelican-themes project, one line for each theme. 
See the little minus sign before the commit hash on each line? That means that the submodule for that theme
is not initialized. We could initialize all the themes, but that would pull down a lot of code I'm not interested
in. I just want a few themes.

    git submodule init blue-penguin
    git submodule init pelican-mockingbird
    git submodule update

`git submodule init` initializes the blue-penguin and pelican-mockingbird themes. Then, `git submodule update` clones the missing submodules.

Then edit your `pelicanconf.py` file, and add this line, giving Pelican the appropriate path to your theme. 

    THEME = 'path/to/your/theme'

I'm using the [Blue Penguin](https://github.com/jody-frankowski/blue-penguin) theme. I made a few modifications. I'm not justifying the text, 
and I replaced the dark solarized code formatting with my own format based on the [Pygments](http://pygments.org/docs/styles) 'friendly' style.

Here's some code, to show off the syntax highlighting. 
    
    from pygments.style import Style
    from pygments.token import Keyword, Name, Comment, String, Error, \
         Number, Operator, Generic

    class YourStyle(Style):
        default_style = ""
        styles = {
            Comment:                'italic #888',
            Keyword:                'bold #005',
            Name:                   '#f00',
            Name.Function:          '#0f0',
            Name.Class:             'bold #0f0',
            String:                 'bg:#eee #111'
        }





