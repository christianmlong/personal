"""
    Setup script for the python package containing common utilities and
    functions.
"""

from setuptools import setup, find_packages

setup(
    name="Common",
    version="4.0.0",
    packages=find_packages(),

    install_requires=['pyodbc>=3',
                      ],

    # metadata
    author="Christian Long",
    author_email="christianzlong@gmail.com",
    description="Common framework for applications",
    url='http://christianlong.com',
)
