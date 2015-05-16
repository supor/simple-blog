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
from ...service import CommentService
from .. import admin_bp as admin

COMMENT_STATUSES = [
    {'url': 'all', 'lang': text('global.all'), 'class': 'all'},
    {'url': 'pending', 'lang': text('global.pending'), 'class': 'pending'},
    {'url': 'approved', 'lang': text('global.approved'), 'class': 'approved'},
    {'url': 'spam', 'lang': text('global.spam'), 'class': 'spam'}
]


@admin.route('/comment')
@admin.route('/comment/<status>')
@admin.route('/comment/<status>/<int:page>')
# @security(EDITOR)
def comment_page(page=1, status='all'):
    pagination = CommentService.page(status, page, siteconfig.posts_per_page())
    return render_template('admin//comment/index.html',
                           statuses=COMMENT_STATUSES,
                           status=status,
                           comments=pagination)

@admin.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
# @security(EDITOR)
def comment_edit(comment_id):
    if request.method == 'GET':
        statuses = {
            'approved': text('global.approved'),
            'pending': text('global.pending'),
            'spam': text('global.spam')
        }
        comment = CommentService.get(comment_id)
        print comment
        return render_template('admin/comment/edit.html',
                               comment=comment,
                               statuses=statuses)

    p = request.form.get
    name = p('name')
    email = p('email')
    content = p('content')
    status = p('status')

    name, content = name.strip(), content.strip()

    validator = Validator()
    (validator.check(name, 'min', text('comment.name_missing'), 1)
        .check(content, 'min', text('comment.content_missing'), 1)
     )
    if validator.errors:
        flash(validator.errors, 'error')
        return redirect(url_for('admin.comment_edit', comment_id=comment_id))

    comment = CommentService.update_comment(
        comment_id, name, email, content, status)
    flash(text('comment.updated'), 'success')
    return redirect(url_for('admin.comment_edit', comment_id=comment.id))

@admin.route('/comment/<int:comment_id>/delete')
# @security(EDITOR)
def comment_delete(comment_id):
    CommentService.delete(comment_id)
    flash(text('comment.deleted'), 'success')
    return redirect(url_for('admin.comment_page'))
