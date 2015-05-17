# -*- coding: utf-8 -*-
'''
Created on 2015-5-16

@author: Nob
'''
import hmac
from hashlib import sha1
import uuid

from functools import wraps
from .models import User
from .service import UserService
from flask import g, session, request, abort, redirect, url_for, current_app, render_template


_guest = User(
    'guest', 'email', 'password', 'bio', status=1, role='guest', id=0)

def security(role=None):
    def decorator(f):
        @wraps(f)
        def _decorator(*args, **kw):
            me = g.user
            if me.is_guest() and request.path != 'admin/login':
                return redirect(url_for('admin.login'))
            access = False
            if me.is_root():
                access = True
            elif not me.active():
                access = False
            elif me.role == role:
                access = True
            elif me.is_admin and role in (User.EDITOR, None):
                access = True

            if access:
                return f(*args, **kw)
            else:
                return render_template('admin/403.html')
        return _decorator
    return decorator


def init_user():
    """Load user if the auth session validates."""
    try:
        user = _guest
        if 'auth' in session:
            uid = session['auth']
            user = UserService.get(uid)
        if user is None:
            session.pop('auth', None)
            user = _guest
    except:
        user = _guest
    g.user = user


@wraps
def csrf_protect(f):
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

    return f


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = _secert_signature(
            current_app.config['CSRF_SECRET'], str(uuid.uuid4()))
    return session['_csrf_token']


def _secert_signature(secret, *parts):
    hash = hmac.new(secret, digestmod=sha1)
    for part in parts:
        hash.update(part)
    return hash.hexdigest()
