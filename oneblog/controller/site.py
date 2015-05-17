# -*- coding: utf-8 -*-
'''
Created on 2015-5-15

@author: Nob
'''


from datetime import datetime
from flask import g, request, flash, current_app, make_response, jsonify, abort
from flask import render_template, redirect, url_for, send_from_directory
from werkzeug.contrib.atom import AtomFeed
from ..helper import siteconfig
from ..lang import text
from ..lib.validator import Validator
from ..models import Page, Post
from ..service import PostService, PageService, CommentService
from . import site_bp as site
from .admin.post import post_page


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
            return search()
        slug = slug.split('/')[-1]
        page = PageService.get_by_slug(slug)
    else:
        site_page = siteconfig.get('site_page', 0)
        if site_page == 0:
            return posts()
        else:
            page = PageService.get(site_page)
    if not page:
        abort(404)
    return theme_render('page.html',
                        page_content=page.content,
                        page_title=page.title,
                        page=page)

@site.route('/posts')
@site.route('/posts/<int:page>')
@site.route('/category/<category>')
@site.route('/category/<category>/<int:page>')
def posts(page=1, category=None):
    if page <= 0:
        theme_render('404.html')
    total, posts = PageService.get_published_posts_page(
        page, siteconfig.posts_per_page(), category)
    return theme_render('posts.html',
                        page_title=u'文章列表',
                        post_total=total,
                        posts=posts,
                        page_offset=page)

@site.route('/post/<slug>')
def post(slug):
    post = PostService.get_by_slug(slug)
    if not post:
        return theme_render('404.html')
    return theme_render('article.html',
                        page_title=post.title,
                        article=post,
                        comments=post.comments,
                        category=post.category)

@site.route('/post/comment/<slug>', methods=['POST'])
def post_comment(slug):
    post = PostService.get_by_slug(slug)
    if not post:
        return theme_render('404.html', page_title='Not Found')

    if post and not post.allow_comment:
        return redirect(url_for('site.post', slug=slug))

    p = request.form.get
    name = p('name', default='')
    email = p('email', default='')
    content = p('content', default='')

    name, content, email = name.strip(), content.strip(), email.strip()
    validator = Validator()
    (validator.check(email, 'email', text('comment.email_missing'))
        .check(content, 'min', text('comment.email_missing'), 1)
     )

    if validator.errors:
        flash(validator.errors, 'error')
        return redirect(url_for('site.post', slug=slug))

    status = siteconfig.get(
        'auto_published_comments', False) and 'approved' or 'pending'
    CommentService.add_comment(name, email, content, status, post)
    return redirect(url_for('site.post', slug=slug))

def search():
    key = request.args.get('q')
    page = request.args.get('page', type=int, default=1)
    pages = PostService.search(key, page)
    return theme_render('search.html',
                        page_title='Serach Article',
                        search_term=key,
                        articles=pages)