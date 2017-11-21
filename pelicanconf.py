#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Setting
AUTHOR = 'YF'
SITENAME = 'Everyday One Step Forward'
#SITEURL = 'https://huyunf.github.io'
TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = 'English'

# PATH
PATH = 'content'
STATIC_PATHS = ['blog']
ARTICLE_PATHS = ['blog']
ARTICLE_URL = 'blogs/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blogs/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_PATHS = ['pages']

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
SOCIAL = (('Github', 'https://github.com/huyunf'),
          ('Facebook', 'https://www.facebook.com/'),
          ('Twitter', 'https://twitter.com/'),
         )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# theme
THEME = 'themes/gum'
GITHUB_URL = 'https://github.com/huyunf'
DISPLAY_CATEGORIES_ON_MENU = True

# plugin
PLUGIN_PATHS = ["plugins", "pelican-plugins"]
PLUGINS = ["tag_cloud", "summary","sitemap","neighbors","just_table"]

TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100
TAG_CLOUD_SORTING = 'random'
TAG_CLOUD_BADGE = True

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.7,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# comment from disques
DISQUS_SITENAME = "huyunf"

# google track
GOOGLE_ANALYTICS = 'Tracking ID'

# configure for just table plugin
JTABLE_TEMPLATE = """
<table class="table table-hover">
    {% if caption %}
    <caption> {{ caption }} </caption>
    {% endif %}
    {% if th != 0 %}
    <thead>
    <tr>
        {% if ai == 1 %}
        <th> No. </th>
        {% endif %}
        {% for head in heads %}
        <th>{{ head }}</th>
        {% endfor %}
    </tr>
    </thead>
    {% endif %}
    <tbody>
        {% for body in bodies %}
        <tr>
            {% if ai == 1 %}
            <td> {{ loop.index }} </td>
            {% endif %}
            {% for entry in body %}
            <td>{{ entry }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </tbody>
</table>
"""
JTABLE_SEPARATOR = '|'
