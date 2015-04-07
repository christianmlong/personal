"""
    Setup script for the python package containing the Pick Pack application.
"""

from setuptools import setup, find_packages
setup(
    name = 'CML_Pickpack',
    version = "6.0.0",
    packages = find_packages(),
    include_package_data = True,

    install_requires = ['Twisted>=14.0.0',
                        'nevow',
                        'CML_Common>=4.0.0',
                       ],

    # dependency_links = [
    #     'http://partsappdev.joco.com/downloads/'
    # ],

    # metadata
    author = 'Christian Long',
    author_email = 'christianzlong@gmail.com',
    description = 'Pick Pack Automation',
    url='http://christianlong.com',
)
