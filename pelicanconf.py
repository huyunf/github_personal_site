#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'YF'
SITENAME = 'YF\'s NoteBook'
#SITEURL = 'https://huyunf.github.io'
TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = 'English'

# PATH
PATH = 'content'
STATIC_PATHS = ['blog']
ARTICLE_PATHS = ['blog']
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{slug}.html'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
        )

# Social widget
SOCIAL = (('Google', 'https://www.google.com/'),
          ('Facebook', 'https://www.facebook.com/'),
          ('Twitter', 'https://twitter.com/'),
         )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
