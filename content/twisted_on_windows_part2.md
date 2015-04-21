Title: Twisted on Windows, 2015 Edition: Part 2
Category: Python
Tags:python, twisted, windows
Author: Christian Long
Date: 2015-04-20 16:30
Summary: Part 2 of my series on running an application using Twisted on Windows, in a 2015 style.

#### <a name="recap"></a>Recap


#### Recap

In [Part 1]({filename}/twisted_on_windows.md), we installed [Twisted](https://twistedmatrix.com), and set it up to run inside a virtualenv. Now, we will configure Twisted to run as a Windows service, under a virtual service account.


#### Install NSSM

With [some](http://twistedmatrix.com/pipermail/twisted-python/2011-October/024632.html) [coding](http://www.banquise.org/python/making-and-deploying-a-twisted-project-as-a-service-under-windows/), Twisted applications can run as a [Windows service](https://msdn.microsoft.com/en-us/library/windows/desktop/ms685141%28v=vs.85%29.aspx). However, instead of doing that, I'm running my application under [NSSM](http://nssm.cc/), the Non-Sucking Serivce Manager. This handy application allows you to run any command-line application as a Windows service.

[Download](https://nssm.cc/download) NSSM and unzip it. In this example, I'm using NSSM version 2.24, so the folder name is `nssm-2.24`. Change these intructions as needed to match the version of NSSM you are installing. Move the `nssm-2.24` folder to `C:\Program Files`. Add this to the [system Path](http://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/):

    C:\Program Files\nssm-2.24\win64

Note that we are using the 64-bit version of NSSM, even though the application we are installing is running on 32-bit Python. The 64-bit version of NSSM can manage both 64-bit and 32-bit applications.

The nssm.exe file might be marked as untrusted. You can unblock it by right-clicking on the file and choosing Properties. In the Properties dialog, click Unblock.

![Properties screenshot]({filename}/images/security_zone.png)

[More information](http://weblogs.asp.net/dixin/understanding-the-internet-file-blocking-and-unblocking) about unblocking files in Windows.

#### <a name="about_nssm"></a>More about NSSM

We will use the NSSM command line tools to configure the new service. The NSSM commands look like this:

    nssm [nssm command] [service name] [arguments]

The following commands assume that you have created a virtualenv called "Example", as described in [Part 1]({filename}/twisted_on_windows.md). Change these commands as needed to match the name of your service and your virtualenv. You have to quote paths if they contain spaces.

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
