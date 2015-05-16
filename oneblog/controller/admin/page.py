# -*- coding: utf-8 -*-
'''
Created on 2015-5-16

@author: Nob
'''
from flask import render_template, redirect, url_for, g

from flask import g, request, current_app
from flask import jsonify
from flask import session
from ...flash import flash
from ...lib.validator import Validator
from ...helper import siteconfig
from ...lang import text
from ...service import PageService
from .. import admin_bp as admin

PAGE_STATUSES = {
    'published': text('global.published'),
    'draft': text('global.draft'),
    'archived': text('global.archived'),
}

@admin.route('/page')
@admin.route('/page/<int:page>')
@admin.route('/page/status/<status>')
@admin.route('/page/status/<status>/<int:page>')
# @security(EDITOR)
def page_page(page=1, status='all'):
    pagination = PageService.page(status, page, siteconfig.posts_per_page())
    return render_template('admin/page/index.html',
                           status=status,
                           pages=pagination)

@admin.route('/page/<int:page_id>/edit', methods=['GET', 'POST'])
# @security(EDITOR)
def page_edit(page_id):
    if request.method == 'GET':
        pages = PageService.dropdown(show_empty_option=True)
        page = PageService.get(page_id)
        return render_template('admin/page/edit.html',
                               statuses=PAGE_STATUSES,
                               pages=pages,
                               page=page)

    f = request.form
    parent = f.get('parent')
    name = f.get('name')
    title = f.get('title')
    name = name or title
    slug = f.get('slug')
    content = f.get('content')
    status = f.get('status')
    show_in_menu = f.get('show_in_menu', type=int, default=0)
    show_in_menu = 1 if show_in_menu else 0
    redirect_ = f.get('redirect')

    validator = Validator()
    (validator
        .check(title, 'min', text('page.title_missing'), 2)
        #.check(redirect, 'url', text('page.redirect_missing'))
     )
    if validator.errors:
        flash(validator.errors, 'error')
        return redirect(url_for('admin.page_edit', page_id=page_id))

    page = PageService.update_page(
        page_id, name, title, slug, content, status, redirect_, show_in_menu, parent)
    print page
    print page.status
    return redirect(url_for('admin.page_edit', page_id=page_id))


@admin.route('/page/add', methods=['GET', 'POST'])
# @security(EDITOR)
def page_add():
    if request.method == 'GET':
        pages = PageService.dropdown(show_empty_option=True)
        return render_template('admin/page/add.html',
                               statuses=PAGE_STATUSES,
                               pages=pages)

    f = request.form
    parent = f.get('parent')
    name = f.get('name')
    title = f.get('title')
    name = name or title
    slug = f.get('slug')
    content = f.get('content')
    status = f.get('status')
    show_in_menu = f.get('show_in_menu', type=int)
    show_in_menu = 1 if show_in_menu else 0
    redirect_ = f.get('redirect')

    validator = Validator()
    validator.add(
        'duplicate', lambda key: PageService.is_exist_slug(key) == False)
    (validator
        .check(title, 'min', text('page.title_missing'), 2)
        .check(slug, 'min', text('page.slug_missing'), 3)
        .check(slug, 'duplicate', text('page.slug_duplicate'))
        .check(slug, 'regex', text('page.slug_invalid'), r'^[0-9_A-Za-z-]+$')
        #.check(redirect, 'url', text('page.redirect_missing'))
     )
    if validator.errors:
        flash(validator.errors, 'error')
        pages = PageService.dropdown(show_empty_option=True)
        return render_template('admin/page/add.html',
                               statuses=PAGE_STATUSES,
                               pages=pages)

    page = PageService.add_page(
        parent, name, title, slug, content, status, redirect_, show_in_menu)
    return redirect(url_for('admin.page_page'))

@admin.route('/page/<int:page_id>/delete')
# @security(EDITOR)
def page_delete(page_id):
    PageService.delete(page_id)
    return redirect(url_for('admin.page_page'))
