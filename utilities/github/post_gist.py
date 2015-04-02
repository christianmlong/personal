"""
    Post Gist

    A little utility for posting a file as a GitHub gist.
"""

# pylint: disable=invalid-name

import argparse
import os
from getpass import getpass
from github3 import authorize, login

try:
    # Python 2
    prompt = raw_input
except NameError:
    # Python 3
    prompt = input

CREDENTIALS_FILE = r'C:\Users\Christian Long\.github3_py\credentials'

def main():
    """
    Main function to post a gist to GitHub.
    """
    (filename, description) = parse_arguments()
    session = get_session()
    post_gist(session, filename, description)

def parse_arguments():
    """
    Parse command line. Return arguments.
    """
    argument_parser = argparse.ArgumentParser('Utility to upload gists to github')
    argument_parser.add_argument('filename',
                                 help='Name of the file to upload',
                                )
    argument_parser.add_argument('description',
                                 help='Description of the gist',
                                )
    return (argument_parser.filename, argument_parser.description) # pylint: disable=no-member

def get_session():
    """
    Return a logged-in GitHub session. If no cached authorization is found on
    the local system, this wlll ask the user for username and password, get an
    auth token from GitHub, and cache the auth token.
    """
    token = _id = ''
    try:
        with open(CREDENTIALS_FILE, 'r') as fd:
            token = fd.readline().strip()
            _id = fd.readline().strip()
    except IOError:
        (username, password) = get_user_pass()
        auth = get_auth_token_for_gists(username, password)
        token = auth.token
        _id = auth.id
        with open(CREDENTIALS_FILE, 'w') as fd:
            fd.write(token + '\n')
            fd.write(_id)

    return login(token=token)

def get_auth_token_for_gists(username, password):
    """
    Log in to GitHub and get an OAuth token for saving gists.
    """
    note = 'githubpy3.py for my utility scripts.'
    scopes = ['gist']
    return authorize(username, password, scopes, note)

def get_user_pass():
    """
    Get the user's username and password.
    """
    username = prompt("Enter GitHub username")

    password = ''
    while not password:
        password = getpass('Password for {0}: '.format(username))

    return (username, password)

def post_gist(session,
              filename,
              description,
             ):
    """
    Post the gist to GitHub
    """
    with open(filename, 'r') as fd:
        gist_text = fd.read

    files = {filename,
        {'content' : gist_text},
    }

    gist = session.create_gist(description, files, public=False)
    # gist = session.create_gist(description, files)

    print(gist.html_url)



if __name__ == '__main__':
    main()
