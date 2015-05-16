# -*- coding: utf-8 -*-
'''
Created on 2015-5-15

@author: Nob
'''

from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for, jsonify
from flask import session
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

