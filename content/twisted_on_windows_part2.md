Title: Twisted on Windows, 2015 Edition: Part 2
Category: Python
Tags:python, twisted, windows
Author: Christian Long
Date: 2015-04-10 12:51
Summary: Part 2 of my series on running an application using Twisted on Windows, in a 2015 style.

#### <a name="recap"></a>Recap

In [Part 1](), we installed [Twisted](https://twistedmatrix.com), and set it up to run inside a virtualenv. Now, we will configure Twisted to run as a Windows service, under a virtual service account.


#### <a name="install_nssm"></a>Install NSSM

With [some coding](), Twisted applications can run as a [Windows service](). However, instead of doing that, I'm running my application under [NSSM](http://nssm.cc/), the Non-Sucking Serivce Manager. This handy application allows you to run any command-line application as a Windows service.

[Download]() NSSM and unzip it. In this example, I'm using NSSM version 2.24, so the folder name is `nssm-2.24`. Change these intructions as needed to match the version of NSSM you are installing. Move the `nssm-2.24` folder to `C:\Program Files`. Add this to the system Path:

    C:\Program Files\nssm-2.24\win64

Note that we are using the 64-bit version of NSSM, even though the application we are installing is running on 32-bit Python. The 64-bit version of NSSM can manage both 64-bit and 32-bit applications.

#### <a name="about_nssm"></a>More about NSSM

We will use the NSSM command line tools to configure the new service. The NSSM commands look like this:

    nssm [nssm command] [service name] [arguments]

The following commands assume that you have created a virtualenv called "Example", as described in [Part 1](). Change these commands as needed to match the name of your service and your virtualenv. You have to quote paths if they contain spaces. 

#### <a name="create_service"></a>Create the Windows service

Start a new admin command prompt (Win-x then a):

    nssm install my_service C:\PythonEnvs\Example\Scripts\python.exe "C:\PythonEnvs\Example\Scripts\twistd.py --python my_tacfile.tac"

This will install a service called my_service. 

Look at the paths in the command above. Instead of specifying the system-wide `python.exe` (C:\Python27\python.exe), we give the path to a `python.exe` in the Scripts folder of our virtual environment. This has the same effect as calling `activate` in an interactive session. The Python interpreter will have access to all the packages installed in that virtual environment.

We also have to specify the full path to `twistd.py`. This file comes with Twisted; it starts the server process.

#### <a name="working_dir"></a>Configure the working directory

The Windows service has been created, but we still need to configure it. Stay in the admin command prompt, and type:

    nssm set my_service AppDirectory C:\PythonEnvs\Example\Lib\site-packages\my_app

In the above example, replace `my_app` with your app name (it's the name you used when you did `pip install`). Check that directory, it should contain your `.tac` file. 

By setting the `AppDirectory` config variable, we are telling NSSM to make that directory the current working directory before starting the service. That is why we did not need to specify the full path to `my_tacfile.tac` when we installed the service.


#### <a name="name_desc"></a>Set display name and directory

    nssm set my_service DisplayName "My App"
    nssm set my_service Description "My sweet application - running as a Windows service!"

The display name and description will show up in the Windows service Manager console #TODO insert screenshot.


#### <a name="set_startup"></a>Configure startup

    nssm set my_service Start SERVICE_DELAYED_AUTO_START

This setting tells the Windows service to start automatically when the server restarts. The NSSM docs have [more information]() about the possible startup options.


#### <a name="which_account"></a>Which account should we use?

There are a number of accounts you can use to run your Windows service. It is a good idea to run network services under the least-privileged account possible. For that reason, a user account is not a good choice. 

Windows provides some built-in accounts for this purpose: 

* The LOCAL_SYSTEM account is still quite privileged. 

* The NETWORK_SERVICE account allows the service to access network resources on the Windows network. However, we don't need to run as the NETWORK_SERVICE account if we are just serving local resources. 

* The LOCAL_SERVICE account has traditionally been the account Windows sysadmins used for services. It does, however, have some drawbacks. There is only one LOCAL_SERVICE account per machine. Let's say you want to set up multiple services per server (a database and a web server, for example). If you assign permissions to the LOCAL_SERVICE account for the benefit of one service, those permissions are shared by all the services that use that account. 

In Windows Server 2008, Microsoft introduced a new kind of account for this purpose, called a "Virtual Service Account". These accounts are automatically created, one for each Windows service. By default, they have few privileges. And, if you assign privileges to a virtual service account, those privileges apply only to that service and that account, Other services on the same machine do not get those privileges.

Virtual service accounts are not especially well documented. The best information I found was in the [SQL Server 2008]() documentation. There's no conveniently-located anchor tag in that document, so scroll down to the section titled "".



#### <a name="set_account"></a>Set account

Because of the advantages listed above, I use virtual service accounts to run my Twisted services on Windows 2012 R2. Virtual service accounts are available on Windows Server 2008 and later. 

NSSM can not currently configure services to use virtual service accounts. I contacted the developer, and he said he is interested in adding support.

However, we can use good old `sc` to configure the service to use the virtual service account. `sc` is the service manager command line utility that comes with Windows. 

    sc config my_service obj= "NT SERVICE\my_service"

Yes, that is a space after the equals sign. `sc` is very particular. SS64 has a good [reference for `sc`]().

Use `nssm` to do most of the configuration, and then use `sc` at the end to set the service to use the virtual service account. `nssm` will complain if you use it to configure a service that has been set to use a virtual service account. If you want to use `nssm`, you can just use `sc` to set the account back to :wq

















#TODO Link to Part 2 from Part 1




















#### <a name="upgrade_pip"></a>Upgrade pip and virtualenv

The Python 2.7.9 installer now includes pip and virtualenv, and sets them up for you by default. However, it does not come with the very latest pip and virtualenv. Here's how to upgrade them to the latest versions.

Start an admin command prompt. On Windows 8 and newer, Win-x then a is a quick keyboard shortcut to open an admin command prompt.

Upgrade pip to  the latest version.

    python -m pip install --upgrade pip

Upgrade virtualenv to the latest version.

    pip install --upgrade virtualenv

Now close the admin command prompt. We will be installing the rest of the packages in to a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), and that does not require admin access. The great advantage of using a virtualenv is that it keeps the packages we install isolated from each other, and from the system-wide packages.


#### <a name="set_up_virtualenv"></a>Set up a virtual environment

Start a regular (non-admin) command prompt. Win-x then c is a quick keyboard shortcut for a non-admin command prompt.

    mkdir C:\PythonEnvs
    virtualenv C:\PythonEnvs\Example
    C:\PythonEnvs\Example\Scripts\activate.bat

This makes a new directory on the C: drive, makes a new virtualenv, and then activates the new virtualenv. You should see the name of the virtualenv in parentheses at the start of your command prompt, something like this:

    (Example) C:\Users\Me>

When a virtualenv is activated, it looks for installed Python packages in its own site-packages directory `C:\PythonEnvs\Example\Lib\site-packages`, instead of looking in the system wide site-packages directory `C:\Python27\Lib\site-packages`. Note that we don't need to be in the virtualenv directory for it to be active.

The [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) project is full of useful shortcuts for working with virtualenvs. For simplicity, I will be using only virtualenv, and not virtualenvwrapper, in this writeup. However, if you're interested in setting up virtualenvwrapper, [this patched version](https://github.com/christianmlong/virtualenvwrapper-win) works on Windows with the latest version of virtualenv.


#### <a name="python_packaging"></a> The state of Python packaging in 2015

Installing Python packages on Windows has gotten a lot easier over the years. The [Python Package Index](https://pypi.python.org/pypi) (PyPI) now provides pre-compiled binary installers in the [wheel](https://wheel.readthedocs.org/en/latest/) format for many packages.

When a wheel is not available, pip can automatically compile C extensions using [this compiler](http://www.microsoft.com/en-us/download/details.aspx?id=44266) that Microsoft provides at no cost.

However, there are still packages that are not available on PyPI. Many are distributed for Windows in the Windows installer format (.msi or .exe). Pip can not install these packages, but there [is a way](#install_from_elsewhere) to install them in to a virtualenv.

#### <a name="install_twisted"></a> Install Twisted

    pip install Twisted

This will pull the latest version from PyPI. It will also install its dependencies. One dependency, `zope.interface`, will use the compiler to compile a C extension.

    . . .
    Installing collected packages: zope.interface, Twisted
      Running setup.py install for zope.interface
        building 'zope.interface._zope_interface_coptimizations' extension
    . . .

If you get a vcvarsall error, [install the Microsoft Visual C++ compiler](#install_compiler).

#### <a name="install_from_pypi"></a> Install dependencies from PyPI

Install pywin32.

    pip install pypiwin32

As of March 2015, pywin32 [is available on PyPI](https://pypi.python.org/pypi/pypiwin32) in the wheel format. That means it can be installed by pip. Note that in order to get the PyPI version, we must tell pip to install package `pypiwin32`, not `pywin32`.


#### <a name="install_from_elsewhere"></a> Install dependencies that are not on PyPI

For packages that are not on PyPI, the installation steps are different. If the package is distributed using a Windows binary installer (.msi or .exe) we can use the older `easy_install` command to install it in to a virtualenv.

One such package is [pyodbc](https://code.google.com/p/pyodbc/), which my application uses to talk to the database. Twisted itself does not depend on pyodbc, so there is no need to install it if your application doesn't use it.

As of March 2015, pyodbc is not available in wheel format from PyPI.
[Download](https://code.google.com/p/pyodbc/downloads/detail?name=pyodbc-3.0.7.win32-py2.7.exe&can=2&q=) the Windows installer. Make sure to get the installer that matches your version of Python and your architecture. I am using this one "3.0.7 32-bit Windows Installer for Python 2.7".

Use `easy_install` to install pyodbc in to the virtualenv from the executable Windows installer file.

    easy_install --always-unzip C:\Path\to\pyodbc-3.0.7.win32-py2.7.exe

I'll talk about why we need `--always-unzip` in Part 2.

Not all installers will work with `easy_install` this way. See this [Stack Overflow question](http://stackoverflow.com/questions/25984095/install-pysvn-in-a-virtualenv/25984096#25984096) for more details.


#### <a name="install_app"></a> Install your application

Whatever Twisted application you are going to be running on this server, install it as you normally would. For example `pip install my_app`.

Now that everything has been installed, check it.

    pip freeze

should look something like this:

    my_app==4.14.2
    pypiwin32==219
    Twisted==14.0.2
    zope.interface==4.1.2
    other dependencies here
    . . .

Newer versions of some of these packages may since have been released.


#### <a name="run_it"></a> Run it

Try it out.

    python C:\PythonEnvs\Example\Scripts\twistd.py --help

The virtualenv picks up the right Python path, but on Windows we have to specify the full path to the `twistd.py` file. This command should give you a nice help message and no errors.

Now try running your app under Twisted.

    python C:\PythonEnvs\Example\Scripts\twistd.py ^
       --rundir "C:\PythonEnvs\Example\Lib\site-packages\my_app" ^
       --python "my_tacfile.tac"

For readability, I have broken this long command in to multiple lines using `^`, the dos line-continuation character.

This command should print out some lines showing the `twistd` server starting up. Again, on Windows, we have to specify the full path to the app install directory when starting the `twistd` server. Go try out your app, and press Ctrl-c to shut down the server when you're done.


#### <a name="up_running"></a> Up and running

That's it for Part 1. We have installed Python, set up a virtualenv, and gotten your Twisted app up and running. In Part 2, we will set up a Windows service to run the app, using the virtual service account that was introduced in Windows Server 2008. In Part 3, we will package the app and its dependencies for deployment to test and production servers. Thanks for reading, and if you have any questions or suggestions, let me know. I'm on Twitter at [@christianmlong](https://twitter.com/christianmlong).
