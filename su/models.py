# -*- coding:utf-8 -*-
from su.extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now())
    cid = db.Column(db.Integer, db.ForeignKey('category.id'))

    comments = db.relationship('Comment', backref='article', lazy='dynamic')

    def __init__(self, cid, title, content):
        self.cid = cid
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Article %r>' % self.content

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20))
    content = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, default=datetime.now())

    aid = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __init__(self, aid, author, content):
        self.aid = aid
        self.name = author
        self.content = content

    def __repr__(self):
        return '<Comment %r>' % self.content

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    sort = db.Column(db.Integer, default=0)# 分类排序，值越大越靠前
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __init__(self, name, sort):
        self.name = name
        self.sort = sort

    def __repr__(self):
        return '<Category %r>' % self.name
