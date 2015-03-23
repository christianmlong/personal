Title: Pelican Blog Workflow
Category: Python
Tags: pelican
Author: Christian Long
Summary: Some tips for using Pelican quickly

This blog is running on [Pelican](http://docs.getpelican.com). It's pretty slick, and here are a few tips I use to make writing and publishing faster and easier.

#### New post

I have this shell script accessible via an alias `nbp`.

    #!/bin/bash

    set -eu

    DRAFTS_DIR=~/projects/personal/blog/drafts

    if [ -z "$1" ] ; then
            FILE_NAME='new_post'
    else
            FILE_NAME="$1"
    fi

    SKEL_FILE=$DRAFTS_DIR/skeleton_post
    FILE_PATH=$DRAFTS_DIR/"$FILE_NAME".md

    cp --no-clobber $SKEL_FILE $FILE_PATH
    vi $FILE_PATH

This copies my posting template to a new file in the drafts directory, and opens it for editing in vim.

#### Dev server

Run this command to start the Pelican development server.

    make devserver

This will automatically regenerate the site when files are changed. It will also serve the site at [http://localhost:8000](http://localhost:8000).

Run `develop_server.sh stop` to stop the development server.

#### Browser auto refresh

There are many auto-refresh solutions for the browser, but they don't work well when you are editing a file on a remote server. [live.js](http://www.livejs.com/) is a nice solution that takes care of auto-refreshing in javascript. However, we don't want to include the live.js javascript file in the published version, just in the local development version. We can modify our theme to include it only when developing.

First edit pelicanconf.py. Add this

    IS_DEVELOPMENT_VERSION = True

Also edit publishconf.py. Add this

    IS_DEVELOPMENT_VERSION = False

Now, change the theme so that every article page includes the live.js javascript, if we are in development. Find your theme's template directory. It's probably at `themes/\<theme name>/templates. Edit `article.html`. Look for the head block in the template `{% block head %}`. Add this to it

    {% if IS_DEVELOPMENT_VERSION %}
      <script type="text/javascript" src="http://livejs.com/live.js"></script>
    {% endif %}

Run `make devserver`, and open [http://localhost:8000](http://localhost:8000). Edit one of your articles, and see if it reloads in the browser automatically. Neat!

The nice thing about the live.js solution is that it works even if the files you are editing are on a remote server. It polls the page by making a head request every few seconds. Obviously, you don't want this polling to happen on your published pages.

