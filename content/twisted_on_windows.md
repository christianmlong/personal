Title: Twisted on Windows, 2015 Edition
Category: Python
Tags:python, twisted, windows
Author: Christian Long
Date: 2015-03-23 17:55
Summary: Install and run an application using Twisted on Windows, in a 2015 style.

#### <a name="intro"></a>Intro

Installing and configuring [Twisted](https://twistedmatrix.com) on Windows has gotten easier over the years. Here is how to do it in 2015, using the latest packaging tools.

Twisted runs well on Windows, in my experience. I moved some Twisted applications from Linux to Windows for a client, and they have been running happily for months now without issue.

These instructions have been tested with Windows 8.1 and Windows Server 2012 R2. The applications I moved use Twisted.Web to serve single-page web apps, talking to a database using [pyodbc](https://code.google.com/p/pyodbc/). My ODBC driver is 32-bit, so I'm using 32-bit Python for these instructions.


#### <a name="install_python"></a>Install Python

Twisted requires Python 2. Install the [latest version](https://www.python.org/downloads/release/python-279/) of Python 2.7 ([direct link to the 32-bit installer](https://www.python.org/ftp/python/2.7.9/python-2.7.9.msi)). Run the installer, and in the installer dialog, choose the option to add python to the path.


#### <a name="install_compiler"></a>Install a compiler

Some of Twisted's dependencies have C extensions, and these packages are not available from the [Python Package Index](https://pypi.python.org/pypi) in the binary `wheel` format. So, you need a compiler to compile them from source. This used to be [tricky](http://stackoverflow.com/questions/2817869/error-unable-to-find-vcvarsall-bat), but fortunately, Microsoft now provides a free download that makes it easy. Download the [Microsoft Visual C++ Compiler for Python 2.7](http://www.microsoft.com/en-us/download/confirmation.aspx?id=44266). It may need to be installed as admin, to get around policy restrictions on compilers.


#### <a name="upgrade_pip"></a>Upgrade pip and virtualenv

The Python 2.7.9 installer now includes pip and virtualenv, and sets them up for you by default. However, it does not come with the very latest pip and virtualenv. Here's how to upgrade them to the latest versions.

Start an admin command prompt. On Windows 8 and newer, 'Win-x then a' is a quick keyboard shortcut to open an admin command prompt.

Upgrade pip to  the latest version.

    python -m pip install --upgrade pip

Upgrade virtualenv to the latest version.

    pip install --upgrade virtualenv

Now close the admin command prompt. You will be installing the rest of the packages in to a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), and that does not require admin access. The great advantage of using a virtualenv is that it keeps the packages we install isolated from each other and from the system-wide packages.


#### <a name="set_up_virtualenv"></a>Set up a virtual environment

Start a regular (non-admin) command prompt. Win-x then c is a quick keyboard shortcut for a non-admin command prompt.

    mkdir C:\PythonEnvs
    virtualenv C:\PythonEnvs\Example
    C:\PythonEnvs\Example\Scripts\activate.bat

This makes a new directory on the C: drive, makes a new virtualenv, and then activates the new virtualenv. You should see the name of the virtualenv in parentheses at the start of your command prompt, something like this:

    (Example) C:\Users\Me

When a virtualenv is activated, it looks for installed Python packages in its own site-packages directory `C:\PythonEnvs\Example\Lib\site-packages`, instead of looking in the system wide site-packages directory `C:\Python27\Lib\site-packages`. Note that we don't need to be in the virtualenv directory for it to be active.

The [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) project is full of useful shortcuts for working with virtualenvs. For simplicity, I will be using only virtualenv, and not virtualenvwrapper, in this writeup. However, if you're interested in setting up virtualenvwrapper, [this patched version](https://github.com/christianmlong/virtualenvwrapper-win) works on Windows with the latest version of virtualenv.

#### <a name="install_into_venv"></a> Install dependencies in to the virtual environment

With the virtuaenv activated, install the `wheel` package, and upgrade `setuptools`.

    pip install --upgrade wheel setuptools

Later I will use `wheel` to create my own binary packages for distribution to my production environment. That way I don't have to install the Microsoft Visual C++ Compiler on my production servers.

Install Twisted.

    pip install Twisted

This will pull the latest version from PyPI. It will also install its dependencies. One dependency, `zope.interface`, will use the compiler to compile a C extension.

    . . .
    Installing collected packages: zope.interface, Twisted
      Running setup.py install for zope.interface
        building 'zope.interface._zope_interface_coptimizations' extension
    . . .

If you get a vcvarsall error, [install the Microsoft Visual C++ compiler](#install_compiler).

Install pywin32.

    pip install pypiwin32

As of January 2015, pywin32 is available on PyPI in the wheel format. That means it can be installed by pip. Note that in order to get the PyPI version, you must tell pip to install package `pypiwin32`, not `pywin32`.

Install [pyodbc](https://code.google.com/p/pyodbc/)

As of January 2015, pyodbc is not available in wheel format from PyPI.
[Download](https://code.google.com/p/pyodbc/downloads/detail?name=pyodbc-3.0.7.win32-py2.7.exe&can=2&q=) the Windows installer. Make sure to get the installler that matches your version of Python and your architecture. I am using this one "3.0.7 32-bit Windows Installer for Python 2.7".

Use easy_install to install pyodbc in to the virtualenv from the Windows installer file.

    easy_install --always-unzip C:\Path\to\pyodbc-3.0.7.win32-py2.7.exe

I'll talk about why we need `--always-unzip` [later](#virtual_service_account)

Install the application.

Whatever Twisted application you are going to be running on this server, install it as you normally would. For example `pip install my_app`.

Now that everything has been installed, check it.

    pip freeze

should look something like this:

    my_app==4.14.2
    pyodbc==3.0.7
    pypiwin32==219
    Twisted==14.0.2
    wheel==0.24.0
    zope.interface==4.1.2

Newer versions of some of these packages may since have been released.


#### <a name="run_it"></a> Run it

Try it out.

    python C:\PythonEnvs\Example\Scripts\twistd.py --help

The virtualenv picks up the right Python path, but on Windows we have to specify the full path to the `twistd.py` file. This command should give you a nice help message and no errors.

Now try running your app under twisted.

    python C:\PythonEnvs\Example\Scripts\twistd.py ^
       --rundir "C:\PythonEnvs\Example\Lib\site-packages\my_app" ^
       --python "my_tacfile.tac"

This should print out some lines showing the `twistd` server starting up. Again, on Windows, you have to specify the full path to your app install directory when starting the `twistd` server. Go try out your app, and press Ctrl-c to shut down the server when you're done.


#### <a name="up_running"></a> Up and running

That's it for part 1. We have installed Python, set up a virtualenv, and gotten a Twisted app up and running. In Part 2, we will set up a Windows service to run the app, using the virutal service account that was introduced in Windows server 2008. Thanks for reading, and if you have any questions or suggestions, let me know. I'm on Twitter at [@christianmlong](https://twitter.com/christianmlong).
