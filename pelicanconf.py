#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

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

DEFAULT_PAGINATION = 10
DEFAULT_DATE = 'fs'

_THEME_BASE = '/home/christianmlong/projects/external/pelican-themes/'
#THEME = _THEME_BASE + 'tuxlite_tbs'
#THEME = _THEME_BASE + 'pelican-mockingbird'
THEME = _THEME_BASE + 'built-texts'


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

#TYPOGRIFY = True
TYPOGRIFY = False

SLUGIFY_SOURCE = 'title'

 #
#

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    }




















#
