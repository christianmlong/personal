
#### <a name="install_wheel"></a> Install wheel

With the virtualenv activated, install the `wheel` package, and upgrade `setuptools`.

    pip install --upgrade wheel setuptools

The `wheel` package is not needed for installing wheels. Rather, it lets you create your own binary packages in the wheel format. In Part 3, we will use `wheel` to create our own binary packages for distribution to the production environment. That way we don't have to install the Microsoft Visual C++ Compiler on the production servers.


#### <a name="install_application"></a> Install your application

