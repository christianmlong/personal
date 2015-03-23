#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Christian Long'
SITENAME = u"Christian Long's Blog"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None


# Blogroll
LINKS = (('Archives', 'archives.html'),
        )

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/christianmlong'),
         )

GITHUB_URL = 'https://github.com/christianmlong'

DEFAULT_PAGINATION = 10
DEFAULT_DATE = 'fs'

_THEME_BASE = 'themes'
_THEME_NAME ='blue-penguin'
THEME = os.path.join(_THEME_BASE, _THEME_NAME)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

DEFAULT_CATEGORY = ('Articles')
#COPYRIGHT = 'Copyright Christian Long 2014'

STATIC_PATHS = ['images',
                'pages',
                'pdfs',
                #'extra',
                'extra/robots.txt',
               ]
PAGES_PATHS = ['pages']

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
TYPOGRIFY = True
SLUGIFY_SOURCE = 'title'

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    }

# Don't regenerate unmodified content. Just use
# the cached version
LOAD_CONTENT_CACHE = True

# Development server version vs published version
# This is used in my theme
IS_DEVELOPMENT_VERSION = True




#
