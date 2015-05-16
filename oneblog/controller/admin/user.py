# -*- coding: utf-8 -*-
'''
Created on 2015-5-15

@author: Nob
'''

from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for, jsonify
from flask import session
from ...lang import text
from ...helper import siteconfig
from ...models import User
from ...service import UserService
from .. import admin_bp as admin

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if g.user.is_guest():
            return render_template('admin/user/login.html')
        return redirect(url_for('admin.post_page'))

    username = request.form['username']
    password = request.form['password']
    user = UserService.auth(username, password)
    if user:
        UserService.login(user)
        return redirect(url_for('admin.post_page'))
    flash(u'登录失败，请检查用户名和密码', 'error')
    return redirect(url_for('admin.login'))


@admin.route('/logout', methods=['GET'])
def logout():
    UserService.logout()
    return redirect(url_for('admin.login'))

@admin.route('/user.json')
def user_json():
    return jsonify(g.user)


@admin.route('/user')
@admin.route('/user/<int:page>')
# @security()
def user_page(page=1):
    me = g.user 
    if me.is_root():
        page = UserService.page(page, siteconfig.posts_per_page())
    else:
        page = UserService.get_user_page(me)
    return render_template('admin/user/index.html', users=page)


@admin.route('/user/add', methods=['GET', 'POST'])
# @security(ROOT)
def user_add():
    if request.method == 'GET':
        return render_template('admin/user/add.html', statuses=User.STATUSES, roles=User.ROLES)

    p = request.form.get
    username = p('username')
    email = p('email')
    real_name = p('real_name')
    password = p('password')
    bio = p('bio')
    status = p('status', default='inactive')
    role = p('role', default='user')

    result = UserService.add_user(
        username, email, password, bio, status, role)
    if result['status'] == 'ok':
        return redirect(url_for('admin.user_edit', uid=result['user'].uid))
    else:
        flash(result['errors'], 'error')
        return render_template('admin/user/add.html', statuses=User.STATUSES, roles=User.ROLES)


@admin.route('/user/<int:uid>/edit', methods=['GET', 'POST'])
# @security()
def user_edit(uid):
    if (not (g.user.is_root() or g.user.is_admin())) and g.user.uid != uid:
        return render_template('admin/403.html', message='You can only edit your self')
    if request.method == 'GET':
        user = UserService.get(uid)
        return render_template('admin/user/edit.html', statuses=User.STATUSES, roles=User.ROLES, user=user)

    p = request.form.get
    email = p('email')
    real_name = p('real_name')
    password = p('password', default='')
    newpass1 = p('newpass1')
    newpass2 = p('newpass2')
    bio = p('bio')
    status = p('status', default='inactive')
    role = p('role', default='user')

    # 验证新旧密码和确认密码
    result = UserService.update_user(uid, email, newpass1, bio, status, role)
    if result['status'] == 'ok':
        return redirect(url_for('admin.user_edit', uid=result['user'].uid))
    else:
        flash(result['errors'], 'error')
        return redirect(url_for('admin.user_edit', uid=uid))

@admin.route('/user/<int:user_id>/delete')
# @security(ROOT)
def user_delete(user_id):
    UserService.delete(user_id)
    flash(text('user.deleted'), 'success')
    return redirect(url_for('admin.user_page'))