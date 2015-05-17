# -*- coding: utf-8 -*-
'''
Created on 2015-5-15

@author: Nob
'''


from flask import Blueprint

admin_bp = Blueprint('admin', 'admin', url_prefix='/admin')
site_bp = Blueprint('site', 'site')


ADMIN, EDITOR, ROOT = 'admin', 'editor', 'root'

from . import (
    admin,
    site
)
