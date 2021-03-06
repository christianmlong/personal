"""
    Setup script for the python package containing common utilities and
    functions.
"""

from setuptools import setup, find_packages
setup(
    name = "CML_Common",
    version = "4.0.0",
    packages = find_packages(),

    install_requires = [],

    # metadata
    author = "Christian Long",
    author_email = "christianzlong@gmail.com",
    description = "Common framework for applications",
    url='http://christianlong.com',
)
