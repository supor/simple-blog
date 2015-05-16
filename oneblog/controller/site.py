# -*- coding: utf-8 -*-
'''
Created on 2015-5-15

@author: Nob
'''


from datetime import datetime
from flask import g, request, flash, current_app, make_response, jsonify, abort
from flask import render_template, redirect, url_for, send_from_directory
from werkzeug.contrib.atom import AtomFeed

from ..models import Page, Post
from .admin.post import post_page
from . import site_bp as site


def theme_render(tpl, *args, **kw):
    theme = current_app.config.get('THEME', 'default')
    tpl = 'theme/' + theme + '/' + tpl
    return render_template(tpl, *args, **kw)


@site.route('/content/<asset>')
def content_asset(asset):
    return send_from_directory(current_app.config['CONTENT_PATH'], asset)


@site.route('/')
@site.route('/<slug>')
def page(slug=None):
    if slug:
        if slug == 'admin':
            return post_page()
        elif slug == 'search':
            pass

        slug = slug.split('/')[-1]
        page = Page.query.filter_by(slug=slug).first()
    else:
        page = Page.query.get(1)
    print page
    if not page:
        abort(404)
    return theme_render('page.html',
                        page_content=page.content,
                        page_title=page.title,
                        page=page)
