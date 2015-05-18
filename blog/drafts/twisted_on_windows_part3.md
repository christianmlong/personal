Title: Twisted on Windows, 2015 Edition: Part 3
Category: Python
Tags:python, twisted, windows
Author: Christian Long
Date:
Summary: Part 3 of my series on running an application using Twisted on Windows, in a 2015 style.

[TOC]

#### Recap

In [Part 1]({filename}/twisted_on_windows.md), we set up [Twisted](https://twistedmatrix.com). In [Part 2]({filename}/twisted_on_windows_part2.md), we configured Twisted to run as a Windows service. Now, we will assign the right permissions to the account that the service is using.


#### Windows file permissions

Since Windows NT, Windows has implemented file-level security through access control lists. Windows provides [the `icacls` utility](http://ss64.com/nt/icacls.html) to query and set permissions at the command line.

For example

    icacls C:\PythonEnvs\Example /grant "nt service\my_service":(OI)(CI)RX

Let's break this down:

 * `C:\PythonEnvs\Example` - The folder you want to change permissions on
 * `/grant` - Grant rights additively
 * `"nt service\my_service"` - The name of the virtual service account
 * `(OI)(CI)` - Applies the grant recursively to this folder, subfolders, and files.
 * `RX` - Grants Read and Execute access


#### Inheritance mode

Inherited folder permissions are specified as:

 * OI - Object inherit    - This folder and files (no inheritance to subfolders)
 * CI - Container inherit - This folder and subfolders
 * IO - Inherit only      - The ACE does not apply to the current file/directory


These can also be combined:

 *   (OI)(CI)       this folder, subfolders, and files
 *   (OI)(CI)(IO)   subfolders and files only
 *       (CI)(IO)   subfolders only
 *   (OI)    (IO)   files only

So `BUILTIN\Administrators:(OI)(CI)F` means that both files and subfolders will inherit 'F' (Full Control)

Similarly `(CI)R` means folders will inherit 'R' (Read folders only = List permission)

SS64 has a [good reference](http://ss64.com/nt/icacls.html) for the `icacl` options.




#### Troubleshooting permissions

Many Windows admin tasks require the wonderful [Sysinternals](https://technet.microsoft.com/en-us/sysinternals/bb545021.aspx) tools, written by Mark Russinonvich. The first thing I do on a new Windows server is [download the Sysinternals Suite](https://technet.microsoft.com/en-us/sysinternals/bb842062.aspx) and put it on the system path. For this troubleshooting section, I'll be using the [`psexec` tool](https://technet.microsoft.com/en-us/sysinternals/bb897553).

Whenever a service is not working, it's helpful to try running it by hand, in the same user account and environment that the service is trying to run in. As far as I know, there is no way to run commands manually as a virtual service account (`NT SERVICE\my_service`). Put another way, there is no equivalent of `su - <user>` that can be used for virtual service accounts. However, we can approximate it. We can use `psexec` to run commands as the LocalService account (`NT AUTHORITY\LocalService`). It's far from perfect, but if we can get it working under the LocalService account, chances are we can then get it working under a virtual service account.

Let's look at some steps we can take to investigate permissions problems. First, open a new admin command prompt. On Windows 8 and newer, "Win-x then a" is a quick way to open an admin command prompt.


Here's how to execute a single command, under the LocalService account.

    psexec -u "NT AUTHORITY\LocalService" C:\PythonEnvs\Example\Scripts\pip freeze

The `-u` option tells `psexec` what user to run as. The rest of the line is the command that you want `psexec` to run. Notice that we pass the full path to the `pip` inside the virtualenv. `pip freeze` prints a list of the packages that are installed.

If you get a "Couldn't install PSEXESVC service:" error, try running as administrator.

Here's another example.  We're telling Python to import the pyodbc module, and print "ok" if it succeeds.

    psexec -u "NT AUTHORITY\LocalService" C:\PythonEnvs\Example\Scripts\python -c "import odbc; print 'ok'"

Here's how to start a new interactive shell in a new window, running as the LocalService user.

    psexec -u "NT AUTHORITY\LocalService" -i cmd /k

It should look something like this.

![New interactive shell screenshot]({filename}/images/cmd_i.png){: .no_round}

In the new command window, I have used the `whoami` command to show that we are running as NT AUTHORITY\LocalService.

That's not very pretty. If you want to start a new interactive session as a different user, but stay in your current command window, omit the `-i` argument to `psexec`.

    psexec -u "NT AUTHORITY\LocalService" cmd /k

Since Windows does not print the username in the shell prompt, it can be hard to know what user you are running as. Use the `whoami` command to see the current user.

The `whoami /all` command shows a lot of useful information about the user, groups and privileges.


![whoami all screenshot]({filename}/images/whoami_all.png){: .no_round}



Two things to keep in mind when using `psexec` to troubleshoot. One, it must be called from an admin command prompt (Win-x then a). Two, you can not use `psexec` to run commands as a virtual service account.

When I'm setting up Windows service, I configure it to run under the LocalService account at first, and I use `psexec` to track down any permissions errors. Then I switch the service over to a virtual service account. I grant the virtual service account the same privileges that I had to grant to the LocalService account to get it working.





#### Zip files

You may find that the virtual service accounts you're using to run the services don't have permission to handle zip files. This may be due to a policy restriction set by your network administrator. The LocalService account may have the same restriction.

This is why, when I'm installing pyodbc, I have to pass --always-unzip to easy_install so that the virtual service account can import pyodbc. Otherwise, easy_install installs it as a zip file, and the virtual service account can't import it.

Another example: on Windows, distutils packages source distributions as zip files. Let's say for example you're running python's [simpleHTTPServer](https://docs.python.org/2/library/simplehttpserver.html) as a Windows service (using nssm), running it as account "nt service\package_server". You can visit http://localhost:8000 and you get a nice file listing. However, if you try to download one of the zip files, you get a 404. Assigning permissions for "nt service\package_server" doesn't work - the permissions apply to folders and text files but they don't apply to zip files through inheritance. It only works if you assign read permission specifically for the zip file itself.

Here's a command to specifically assign permissions for a zip file

     icacls "C:\PackageServer\www\downloads\My_Package-0.0.1.zip" /grant "nt service\package_server":R






#### By your leave


We've come to the end of Part 3.  The virtual service account under which the service is running has been assigned the permissions it needs. Thanks for following along, and find me on Twitter at [@christianmlong](https://twitter.com/christianmlong) if you have any suggestions or fixes.
