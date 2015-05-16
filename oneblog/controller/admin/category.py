# -*- coding: utf-8 -*-
'''
Created on 2015-5-15

@author: Nob
'''

from flask import render_template, redirect, url_for

from flask import g, request, current_app, flash
from flask import jsonify
from flask import session
from ...lib.validator import Validator
from ...lang import text
from ...helper import siteconfig
from ...service import CategoryService
from .. import admin_bp as admin

@admin.route('/category')
@admin.route('/category/<int:page>')
# @security(ADMIN)
def category_page(page=1):
    pagination = CategoryService.page(page)
    return render_template('admin/category/index.html',
                           categories=pagination)

@admin.route('/category/add', methods=['GET', 'POST'])
# @security(ADMIN)
def category_add():
    if request.method == 'GET':
        return render_template('admin/category/add.html')

    reqp = request.form
    title = reqp.get('title')
    slug = reqp.get('slug')
    description = reqp.get('description')

    validator = Validator()
    validator.check(title, 'min', text('category.title_missing'), 1)
    if validator.errors:
        flash(validator.errors, 'error')
        return render_template('admin/category/add.html')

    CategoryService.add_category(title, slug, description)
    return redirect(url_for('admin.category_page'))

@admin.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
# @security(ADMIN)
def category_edit(category_id):
    if request.method == 'GET':
        category = CategoryService.get(category_id)
        return render_template('admin/category/edit.html', category=category)

    p = request.form.get
    title = p('title')
    slug = p('slug')
    description = p('description')

    validator = Validator()
    validator.check(title, 'min', text('category.title_missing'), 1)
    if validator.errors:
        flash(validator.errors, 'error')
        return redirect(url_for('admin.category_edit', category_id=category_id))

    category = CategoryService.update_category(
        category_id, title, slug, description)
    print category
    print category.description
    flash(text('category.updated'), 'success')
    return redirect(url_for('admin.category_edit', category_id=category.id))

@admin.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
# @security(ADMIN)
def category_delete(category_id):
    if category_id == 1:
        flash('The Uncategory cann\'t delete', 'error')
        return redirect(url_for('admin.category_page'))

    CategoryService.delete(category_id)
    flash(text('category.deleted'), 'success')
    return redirect(url_for('admin.category_page'))
