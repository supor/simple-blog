# -*- coding:utf-8 -*-
import sqlite3
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from su.extensions import db
from su.models import User, Article, Comment
from config import Config

home = Blueprint('/', __name__,template_folder='templates')


@home.route('/create_db')
def create_db():
    db.create_all()
    return u"创建数据库"


@home.route('/hello')
def index():
    return "hello"

@home.route('/')
@home.route('/article')
def article_list():
    categoryid = request.args.get('categoryid', None)
    articles = []
    if categoryid is None:
        articles = Article.query.all()
    else:
        articles = Article.query.filter_by(cid = categoryid).all()
    return render_template('articles.html',list=articles)

@home.route('/article/<id>')
def article_detail(id):
    print 'id:',id
    article = Article.query.get(id)
    print article
    return render_template('detail.html', article=article)

@home.route('/article/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        # step 1:
        aid = request.form['aid']
        author = request.form['author']
        content = request.form['content']

        # step 2:验证参数 todo

        # step 3:
        comment = Comment(aid, author, content)

        # step 4:
        db.session.add(comment)
        db.session.commit()
        return redirect('/article/'+aid)
    return redirect('/article')


#登录
@home.route('/login', methods=['GET', 'POST'])
def login():
    print Config.PASSWORD
    error = None
    if request.method == 'POST':
        if request.form['username'] != Config.USERNAME:
            error = 'Invalid username'
        elif request.form['password'] != Config.PASSWORD:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('article_list'))
    return render_template('login.html', error=error)
