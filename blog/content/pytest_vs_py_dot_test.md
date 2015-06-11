Title: pytest vs py.test
Category: Python
Tags: pytest
Author: Christian Long
Date: 2015-06-10 20:12
Summary: The pylint package provides a pytest utility that is easily confused with py.test

[TOC]

#### The Problem

`pylint` installs a `pytest` script, and `pytest` installs a `py.test` script.

The [`pylint`](http://www.pylint.org/) code quality checker installs, as one of its dependencies, the [`logilab-common`](https://www.logilab.org/project/logilab-common) package. `logilab-common` provides a module called `pytest`. That's awfully close to the `py.test` script that the [`pytest`](http://pytest.org) project provides. I can never remember which one to use, when I have both `pylint` and `pytest` installed. Fortunately, the  [`logilab-common`](https://www.logilab.org/project/logilab-common) package has marked its `pytest` module as "to be deprecated", so the confusion might be fixed someday.

#### Investigating using `strace`

I knew the `pytest` project was supplying the `py.test` script, but I did not know where the unwanted `pytest` script was coming from. `strace` to the rescue! 

    $ strace -o trace.txt -e open pytest --help
    $ grep pytest trace.txt

    open("/home/me/.virtualenvs/dev/bin/pytest", O_RDONLY) = 3
    open("/home/me/.virtualenvs/dev/bin/pytest", O_RDONLY) = 3
    open("/home/me/.virtualenvs/dev/local/lib/python2.7/site-packages/logilab/common/pytest.x86_64-linux-gnu.so", O_RDONLY) = -1 ENOENT (No such file or directory)
    open("/home/me/.virtualenvs/dev/local/lib/python2.7/site-packages/logilab/common/pytest.so", O_RDONLY) = -1 ENOENT (No such file or directory)
    open("/home/me/.virtualenvs/dev/local/lib/python2.7/site-packages/logilab/common/pytestmodule.so", O_RDONLY) = -1 ENOENT (No such file or directory)
    open("/home/me/.virtualenvs/dev/local/lib/python2.7/site-packages/logilab/common/pytest.py", O_RDONLY) = 3
    open("/home/me/.virtualenvs/dev/local/lib/python2.7/site-packages/logilab/common/pytest.pyc", O_RDONLY) = 4


Here we see that the `pytest.py` file is in the `logilab/common` directory, so we know what package installed it. 

For a fun intro to `strace`, see Julia Evans' [`strace` zine](http://jvns.ca/blog/2015/04/14/strace-zine/).

