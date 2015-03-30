"""
    Setup script for my pygments code highlighting theme
"""

from setuptools import setup, find_packages
setup(
    name = 'cml_theme',
    version = '1.0',
    packages = find_packages(),
    include_package_data = True,

    install_requires = ['pygments',
                       ],

    # metadata
    author = 'Christian Long',
    author_email = 'christianzlong2@gmail.com',
    description = 'My pygments code highlighting theme',
    url='http://christianlong.com',

    # endpoints
    entry_points = {
        'pygments.styles' : 'cml=cml_theme:CML',
    },
)
