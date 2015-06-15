
import subprocess, sys, string, os, argparse

from cookiecutter.main import cookiecutter

def main():
    """
    Automate the setup of a new virtualenv with
    virtualenvwrapper and cookiecutter
    """
    args = get_args()
    repo_name = cut_cookie(args)
    mkvirtualenv(repo_name)

    # print('=====================')
    # print(repo_name)
    # print('=====================')
    sys.stdout.write(repo_name)
    sys.stdout.flush()
    sys.exit(0)

def get_args():
    """
    Get the arguments
    """
    parser = argparse.ArgumentParser(description='Start a project with a cookiecutter and a virtualenv')
    parser.add_argument('project_name',
                       help='A name for the project')
    parser.add_argument('project_short_description',
                       help='A short description for the project')
    args = parser.parse_args()
    return args

def mkvirtualenv(virtualenv_name):
    """
    Use virtualenvwrapper to make a virtualenv.
    """
    project_dir = '~/projects'
    project_path = os.path.join(project_dir, virtualenv_name)
    shell_command = (
        'source /usr/local/bin/virtualenvwrapper.sh'
        + ' && mkvirtualenv -q %s' % virtualenv_name
        # 'mkvirtualenv %s' % virtualenv_name
        + ' && cd %s' % project_path
        + ' && setvirtualenvproject'
    )
    subprocess.check_output(
        shell_command,
        shell=True,
        executable='/bin/bash',
    )

def cut_cookie(args):
    """
    Call cookiecutter
    """
    repo_name = args.project_name.lower().replace(' ', '-')
    pkg_name = repo_name.replace('-', ' ')
    app_name = pkg_name

    os.chdir(os.path.expanduser('~/projects'))

    cookiecutter(
        os.path.expanduser('~/.cookiecutters/cookiecutter-pypackage'),
        no_input=True,
        extra_context={
            'project_name' : args.project_name,
            'project_short_description' : args.project_short_description,
            'repo_name' : repo_name,
            'pkg_name' : pkg_name,
            'app_name' : app_name,
        }
    )

    return repo_name


if __name__ == '__main__':
    main()
