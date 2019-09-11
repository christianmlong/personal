#!/bin/bash

# Exit right away if there is an error.
set -e

# Throw an error for any uninitialized variables.
set -u


INPUT_FILE=source/example.csv

# Split the CSV file in to separate files, according to
# the value of the first colum. Ignore the header.
awk -F, '{ print > $1 ".csv" }' <(sort <(tail -n+2 $INPUT_FILE))

BASH_NEWLINE=$'\n'
HEADER=$(head -1 "$INPUT_FILE")$BASH_NEWLINE
PERL_COMMAND="print '$HEADER' if $. == 1"

# Add the header back to the resulting split CSV files.
shopt -s nullglob
for f in *.csv
do
    perl -pi -e  "$PERL_COMMAND" "$f"
done
