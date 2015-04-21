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
