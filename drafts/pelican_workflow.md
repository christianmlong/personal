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

This will automatically regenerate the site when files are changed. It will also serve the site at http://localhost:8000

Run `develop_server.sh stop` to stop the development server.

#### Browser auto refresh

There are many auto-refresh solutions for the browser, but they don't work well when you are editing a file on a remote server. [live.js](http://www.livejs.com/) is a nice solution that takes care of auto-refreshing in javascript.
