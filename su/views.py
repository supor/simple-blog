# -*- coding:utf-8 -*-
import sqlite3
from flask import Blueprint, render_template,request,g
from su.extensions import db
from su.models import User, Article


home = Blueprint('/', __name__,template_folder='templates')

# 执行一次就够了
@home.route('/create_db')
def create_db():
    db.create_all()
    return u"创建数据库"


@home.route('/')
def index():

    return "hello"

@home.route('/article_list')
def article_list():
    articles = Article.query.all()
    return render_template('articles.html',list=articles)

@home.route('/article/<aid>/')
def article_detail(aid):
    a = Article.query.get(aid)
    return render_template('article/detail.html', article=a)
