# -*- coding:utf-8 -*-
from hashlib import sha224
from datetime import datetime
from .extensions import db

class User(db.Model):
    STATUSES = {
        'active': 'active',
        'inactive': 'inactive',
    }
# 
#     USER = 'user'
#     ROOT = 'root'
#     ADMIN = 'administrator'
#     EDITOR = 'editor'
    ROLES = {
        # 'root' : 'root',
        'admin': 'admin',
        'editor': 'editor',
        'user': 'user'
    }

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(60), unique=True)
    _password = db.Column('password', db.CHAR(56))
    bio = db.Column(db.Text, default='')
    status = db.Column(db.Integer, default=1) # 0 'inactive', 1 'active'
    role = db.Column(db.Enum('root','admin','editor','user'), default='admin')

    def __init__(self, username, email, password, bio='', status=1, role='user', id=None):
        self.username = username
        self.email = email
        self.bio = bio
        self.status = status
        self.role = role
        if id is not None:
            self.id = id
            self._password = password
        else:
            self._password = self.secure_password(password)

    def inactive(self):
        return self.status == 0
    def is_guest(self):
        return self.id == 0
    def is_root(self):
        return self.id == 1
    def password():
        doc = "The password property."
        def fget(self):
            return self._password
        def fset(self, value):
            self._password = self.secure_password(value)
        def fdel(self):
            del self._password
        return locals()
    password = property(**password())

    def check(self, password):
        """Check the password"""
        return self._password == self.secure_password(password)

    @classmethod
    def secure_password(self, password):
        """Encrypt password to sha224 hash"""
        return sha224(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    slug = db.Column(db.String(60), default='')
    description = db.Column(db.Text, default='')
    sort = db.Column(db.Integer, default=0)# 分类排序，值越大越靠前

    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __init__(self, title, slug, description, sort):
        self.title = title
        self.slug = slug
        self.description = description
        self.sort = sort

    def category_url(self):
        return '/category/' + self.slug
    def category_count(self):
        return Post.query.filter_by(category_id=id).count()
    def __repr__(self):
        return '<Category %r>' % self.title

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    title = db.Column(db.String(120))
    slug = db.Column(db.String(60))
    content = db.Column(db.Text)
    status = db.Column(db.Enum('draft','published','archived'), default='published')
    redirect = db.Column(db.Text)
    show_in_menu = db.Column(db.Integer)
    menu_order = db.Column(db.Integer)

    parent_id = db.Column(db.Integer, default=0) # 0为跟节点
#     parent = db.relationship('Page',lazy='immediate')

    def __init__(self, name, title, slug, content, status='published', redirect='', show_in_menu=1, parent_id=0):
        self.parent_id = parent_id
        self.name = name
        self.title = title
        self.slug = slug
        self.content = content
        self.status = status
        self.redirect = redirect
        self.show_in_menu = show_in_menu

    def url(self):
        segments = [self.slug]
        parent_id = self.parent_id
        while parent_id:
            page = Page.query.filter_by(parent_id=parent_id).first()
            if page:
                segments.insert(0, page.slug)
                parent_id = page.parent_id
            else:
                break
        return '/' + '/'.join(segments)

    def __repr__(self):
        return '<Page %r>' % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    slug = db.Column(db.String(60))
    description = db.Column(db.Text)
    html = db.Column(db.Text)
    css = db.Column(db.Text)
    js = db.Column(db.Text)
    status = db.Column(db.Enum('draft','published','archived'), default='published')
    allow_comment = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User',lazy='immediate')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 双向绑定隐含的category
#     category = db.relationship('Category',lazy='immediate')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self, title, slug, description, html, css, js, category_id, status, allow_comment, author_id):
        self.title = title
        self.slug = slug
        self.description = description
        self.html = html
        self.css = css
        self.js = js
        self.category_id = category_id
        self.status = status
        self.allow_comment = allow_comment
        self.author_id = author_id
    def __repr__(self):
        return '<Post %s, %r>' % (self.id, self.title)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(60))
    content = db.Column(db.Text)
    status = db.Column(db.Enum('pending','approved','spam'), default='pending')
    create_time = db.Column(db.DateTime, default=datetime.now())

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, post_id, name, email, content, status):
        self.post_id = post_id
        self.name = name
        self.email = email
        self.content = content
        self.status = status

    def __repr__(self):
        return '<Comment %r>' % self.content

class Kvstore(db.Model):
    key = db.Column(db.String(140), primary_key=True)
    value = db.Column(db.Text)

    def __init__(self, key, value):
        self.key = key
        self.value = value



