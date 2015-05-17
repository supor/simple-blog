# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .extensions import db

home = Blueprint('home', __name__,static_url_path="/static", template_folder='templates', static_folder='static')


@home.route('/create_db')
def create_db():
    from . import models
    db.create_all()
#     user = models.User(username, email, password, bio='', status=1, role='user', id=None)
    user = models.User('root', 'root@localhost', 'root')
    category = models.Category('个人日记', 1)
    page = models.Page('about', '关于', 'about', '这是一个关于页面')

    db.session.add(user)
    db.session.add(category)
    db.session.add(page)
    db.session.commit()
    return u"创建数据表完成"

@home.route('/hello')
def index():
    return "hello"


