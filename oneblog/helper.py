# -*- coding: utf-8 -*-
'''
Created on 2015-5-16

{
    "auto_published_comments": true, 
    "comment_moderation_keys": [ ], 
    "comment_notifications": false, 
    "description": "Oneblog is a Blog system", 
    "posts_per_page": 10, 
    "site_page": 0, 
    "sitename": "Oneblog"
}

@author: Nob
'''
import json
from .extensions import db
from .models import Category, Page

siteconfigjson = """
{
    "auto_published_comments": true, 
    "comment_moderation_keys": [ ], 
    "comment_notifications": false, 
    "description": "Oneblog is a Blog system", 
    "posts_per_page": 10, 
    "site_page": 0, 
    "sitename": "Oneblog"
}"""

def categories():
    return Category.query.all()

def menus():
    return Page.query.filter_by(show_in_menu=1).all()

class SiteConfig(object):
    def sitename(self):
        return self.config.get('sitename', 'Oneblog')

    def description(self):
        return self.config.get('site_description', '')

    def posts_per_page(self, perpage=10):
        return self.config.get('posts_per_page', perpage)

    def comment_moderation_keys(self):
        return self.config.get('comment_moderation_keys', [])

    def get(self, key, default=None):
        return self.config.get(key, default)

    @property
    def config(self):
        return self._config()

    def _config(self):
        global siteconfigjson
        return json.loads(siteconfigjson)
#         return Backend('storage').find('system').json_value()

siteconfig = SiteConfig()