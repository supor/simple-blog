# -*- coding: utf-8 -*-
'''
Created on 2015-5-15

@author: Nob
'''

from flask import render_template, redirect, url_for, g, flash

from flask import g, request, current_app
from flask import jsonify
from flask import session
from ...lib.validator import Validator
from ...helper import siteconfig
from ...lang import text
from ...service import PostService, CategoryService
from .. import admin_bp as admin

STATUSES = {
    'published': text('global.published'),
    'draft': text('global.draft'),
    'archived': text('global.archived'),
}

@admin.route('/post')
@admin.route('/post/<int:page>')
@admin.route('/post/category/<int:category>')
# @security(EDITOR)
def post_page(page=1, category=None):
    pagination = PostService.page(page, siteconfig.posts_per_page(), category)
    return render_template('admin//post/index.html',
                           categories=CategoryService.dropdown(),
                           posts=pagination,
                           category=category)

@admin.route('/post/add', methods=['GET', 'POST'])
# @security(EDITOR)
def post_add():
    if request.method == 'GET':
        print CategoryService.dropdown()
#         fields = extend_service.get_fields_by_type('post')
        return render_template('admin/post/add.html',
                               statuses=STATUSES,
                               categories=CategoryService.dropdown())

    p = request.form.get
    title = p('title', default='')
    description = p('description')
    category = p('category', type=int, default=1)
    status = p('status', default='draft')
    comments = p('comments', type=int, default=0)
    html = p('html')
    css = p('custom_css', default='')
    js = p('custom_js', default='')
    slug = p('slug')

    title = title.strip()
    slug = slug.strip() or title
    validator = Validator()
    (validator.check(title, 'min', text('post.title_missing'), 1)
        .check(slug, 'min', text('post.title_missing'), 1)
     )
    if validator.errors:
        flash(validator.errors, 'error')
        return render_template('admin/post/add.html')

    author = g.user
    post = PostService.add_post(
        title, slug, description, html, css, js, category, status, comments, author)
#     extend_service.prcoess_field(post, 'post')
    return redirect(url_for('admin.post_page'))

@admin.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
# @security(EDITOR)
def post_edit(post_id):
    if request.method == 'GET':
        return render_template('admin/post/edit.html',
                               statuses=STATUSES,
                               categories=CategoryService.dropdown(),
                               article=PostService.get_by_pid(post_id))

    p = request.form.get
    title = p('title', default='')
    description = p('description')
    category = p('category', type=int, default=1)
    status = p('status', default='draft')
    comments = p('comments', type=int, default=0)
    html = p('html')
    css = p('custom_css', default='')
    js = p('custom_js', default='')
    slug = p('slug')

    title = title.strip()
    slug = slug.strip() or title

    validator = Validator()
    (validator.check(title, 'min', text('post.title_missing'), 1)
        .check(slug, 'min', text('post.title_missing'), 1)
     )
    if validator.errors:
        flash(validator.errors, 'error')
        return redirect(url_for('admin.post_edit', post_id=post_id))

    post = PostService.update_post(
        title, slug, description, html, css, js, category, status, comments, post_id)
    flash(text('post.updated'), 'success')
    return redirect(url_for('admin.post_edit', post_id=post_id))

@admin.route('/post/<int:post_id>/delete')
# @security(EDITOR)
def post_delete(post_id):
    PostService.delete(post_id)
    flash(text('post.deleted'), 'success')
    return redirect(url_for('admin.post_page'))
