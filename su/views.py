# -*- coding:utf-8 -*-
from flask import Blueprint, render_template,request
from su.extensions import db
from su.models import User, Article


fronted = Blueprint('/', __name__,template_folder='templates')

@fronted.route('/article/')
def article_list():
    return 'article_list'

@fronted.route('/article/<aid>/')
def article_detail(aid):
    a = Article.query.get(aid)
    return render_template('article/detail.html', article=a)
