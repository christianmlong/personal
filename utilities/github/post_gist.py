from github3 import authorize, login
from getpass import getpass

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
    args = parse_arguments()

def parse_arguments():
    """
    Parse command line. Return arguments.
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('filename',
                                 help='Name of the file to upload',
                                )
    argument_parser.add_argument('description',
                                 help='Description of the gist',
                                )
    return argument_parser.parse_args()

def get_session():
    """
    Return a logged-in GitHub session. If no cached authorization is found on
    the local system, this wlll ask the user for username and password, get an
    auth token from GitHub, and cache the auth token.
    """
    token = id = ''
    try:
        with open(CREDENTIALS_FILE, 'r') as fd:
            token = fd.readline().strip()
            id = fd.readline().strip()
    except IOError:
        (username, password) = get_user_pass()
        auth = get_auth_token_for_gists(username, password)
        token - auth.token
        id - auth.id
        with open(CREDENTIALS_FILE, 'w') as fd:
            fd.write(token + '\n')
            fd.write(id)

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

if __name__ == '__main':
    main()
