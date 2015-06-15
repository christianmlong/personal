Title: ipdb, the iPython debugger
Category: Python
Tags:python, ipython
Author: Christian Long
Date: 2015-06-15 15:32
Summary: An introduction to ipdb, the iPython debugger.

[TOC]

#### Introduction

Python comes with a very useful debugger called `pdb`. The [iPython](http://ipython.org/) project provides an enhanced version of `pdb` called `ipdb`. The `ipdb` debugger provides the same standard debugging commands as `pdb`, and it includes some nice additional features such as tab completion.

#### Installation

Install `ipdb` from the [Python Package Index](https://pypi.python.org/pypi).

    pip install ipdb

On Windows, you have to install the `pyreadline` library as well

    pip install pyreadline




#### Basic debugging



Let's step through a very simple Python program. Add this to a file called `example.py`



    def main():
        """
        Main function
        """
        x = 34
        y = 3
        z = y/x
        print(x,y,z)

    if __name__ == '__main__':
        main()

Run it, wrapped in the `ipdb` debugger.

    ipdb example.py

If you are using Python 3, the debugger script is called `ipdb3` instead of `ipdb`

    ipdb3 example.py

The debugger starts up, and waits at the first line.

    :::text
    > /home/example.py(1)<module>()
    ----> 1 def main():
          2     """
          3     Main function

First, let's get help on what commands are available. Type `?` and press enter.


    :::text
    ipdb> ?

    Documented commands (type help <topic>):
    ========================================
    EOF    bt         cont      enable  jump  pdef    psource  run      unt
    a      c          continue  exit    l     pdoc    q        s        until
    alias  cl         d         h       list  pfile   quit     step     up
    args   clear      debug     help    n     pinfo   r        tbreak   w
    b      commands   disable   ignore  next  pinfo2  restart  u        whatis
    break  condition  down      j       p     pp      return   unalias  where

    Miscellaneous help topics:
    ==========================
    exec  pdb

    Undocumented commands:
    ======================
    retval  rv


More help is available for each command.


    :::text
    ipdb> ?s
    s(tep)
    Execute the current line, stop at the first possible occasion
    (either in a function that is called or in the current function).

#### Basic usage

Step through the program with `s` until you get past the line where 34 is assigned to `x`.

Now that we're here, let's see what value `x` holds. Type `x` and `ipdb` will display the value of `x`.

Set a breakpoint

    :::text
    ipdb> b 8
    Breakpoint 1 at /home/example.py:8

Use `c` to continue execution until that breakpoint.


Use `q` to quit out of the debugger.



#### iPython additions

`ipdb` adds some useful features above what plain `pdb` provides. The most useful is tab-completion. Any identifiers that are defined in locals() or in globals() can be tab-completed.


The "magic" commands (`%`, `??`) from the regular iPython shell are not available in `ipdb`. Instead, `ipdb` provides some extra debugger commands, prefixed with a "p". `pinfo obj` is the same as `obj?` in the iPython shell.

Step in to `example.py`, past the definition of `main()`. Type `pinfo main`


    :::text
    ipdb> pinfo main
    Signature: main()
    Docstring: Main function
    File:      ~/example.py
    Type:      function

This shows us some useful information about the `main()` function.

`psource` will display the source of an object.

    :::text
    ipdb> psource main
    def main():
        """
        Main function
        """
        x = 34
        y = 3
        z = y/x
        print(x,y,z)



#### Further reading

We have just scratched the surface of `pdb` and `ipdb`. There is good information available right in the debugger,
available by typing `?pdb`.



For more information about plain `pdb` and its commands, the "Python Module of the Week" series did a [nice introduction](http://pymotw.com/2/pdb/).


#### Alternatives

The [`pudb` debugger](https://pypi.python.org/pypi/pudb) presents a more visual display, with separate panes for breakpoints and local variables. It is available on Linux and OS X.

For more intractable problems, the Linux `strace` utility traces all system calls made by a program. It can attach to an already-running process, and can capture all the file and network input and output.

    strace -o output.txt python example.py
    grep example output.txt

This shows us all the occurrences of the word 'example' in the system calls that happen when we run `python example.py`


    execve("/home/.virtualenvs/test/bin/python", ["python", "example.py"], [/* 36 vars */]) = 0
    readlink("example.py", 0x7ffe244a2fe0, 4096) = -1 EINVAL (Invalid argument)
    lstat("/home/example.py", {st_mode=S_IFREG|0664, st_size=135, ...}) = 0
    stat("example.py", {st_mode=S_IFREG|0664, st_size=135, ...}) = 0
    open("example.py", O_RDONLY)            = 3
    stat("example.py", {st_mode=S_IFREG|0664, st_size=135, ...}) = 0
    open("example.py", O_RDONLY)            = 3


Let's remove read permissions for `example.py`

    chmod a-r example.py

If we run our `strace` again, we see that the `open` syscall now returns an error.



    execve("/home/virtualenvs/test/bin/python", ["python", "example.py"], [/* 36 vars */]) = 0
    readlink("example.py", 0x7ffc15852b60, 4096) = -1 EINVAL (Invalid argument)
    lstat("/home/example.py", {st_mode=S_IFREG|0220, st_size=135, ...}) = 0
    stat("example.py", {st_mode=S_IFREG|0220, st_size=135, ...}) = 0
    open("example.py", O_RDONLY)            = -1 EACCES (Permission denied)
    stat("example.py", {st_mode=S_IFREG|0220, st_size=135, ...}) = 0
    open("example.py", O_RDONLY)            = -1 EACCES (Permission denied)
    write(2, "python: can't open file 'example"..., 67) = 67


[Chad Fowler](http://chadfowler.com/blog/2014/01/26/the-magic-of-strace/) and [Julia Evans](http://jvns.ca/blog/categories/strace/) have written good introductions to `strace`.


