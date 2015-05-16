# -*- coding: utf-8 -*-
'''
Created on 2015-5-16

@author: Nob
'''
from datetime import datetime
from flask import session, g
from .lib.paginator import Paginator
from .extensions import db
from .models import User, Post, Category, Comment

class UserService(object):
    @staticmethod
    def auth(username, password):
        user = User.query.filter_by(username=username).first()
        if user and not user.inactive() and user.check(password):
            return user
        return False

    @staticmethod
    def login(user):
        session.permanent = True
        session['auth'] = user.id

    @staticmethod
    def logout():
        session.pop('auth', None)

class PostService(object):
    @staticmethod
    def get_by_pid(id):
        return Post.query.filter_by(id=id).first()

    @staticmethod
    def page(page=1, perpage=10, category_id=None):
        q = Post.query
        if category_id:
            q = q.filter_by(category_id=category_id)
        total = q.count()
        posts = q.paginate(page, perpage, error_out=False).items
        pagination = Paginator(posts, total, page, perpage, '/admin/post')
        return pagination

    @staticmethod
    def add_post(title, slug, description, html, css, js, category, status, allow_comment, author):
        css, js, description = css.strip(), js.strip(), description.strip()
        allow_comment = 1 if allow_comment else 0
        if not html.strip():
            status = 'draft'

        post = Post(title, slug, description, html, css, js, category, status, allow_comment, author.id)
        post.created = datetime.now()
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def update_post(cls, title, slug, description, html, css, js, category_id, status, allow_comment, post_id):
        css, js, description = css.strip(), js.strip(), description.strip()
        post = cls.get_by_pid(post_id)
        if not html.strip():
            status = 'draft'

        post.title = title
        # post.slug = slug
        post.description = description
        post.html = html
        post.css = css
        post.js = js
        post.updated = datetime.now()
        post.category_id = category_id
        post.status = status
        post.allow_comment = 1 if allow_comment else 0

        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def delete(cls, id):
        post = cls.get_by_pid(id)
        if not post:
            return None
        db.session.delete(post)
        db.session.commit()

class CategoryService(object):
    @staticmethod
    def dropdown():
        """Returns the all category id"""
        return Category.query.all()

class CommentService(object):
    @staticmethod
    def get(id):
        return Comment.query.filter_by(id=id).first()

    @staticmethod
    def page(status, page=1, perpage=10):
        q = Comment.query
        if status and status != 'all':
            print status
            q = q.filter_by(status=status)
        total = q.count()
        comments = q.paginate(page, perpage, error_out=False).items
        pagination = Paginator(comments, total, page, perpage, '/admin/comment')
        return pagination

    @classmethod
    def update_comment(cls, comment_id, name, email, content, status):
        comment = cls.get(comment_id)
        if not comment:
            return None
        comment.status = status
        comment.name = name
        comment.content = content
        comment.email = email
        db.session.add(comment)
        db.session.commit()
        return comment

    @classmethod
    def delete(cls, comment_id):
        comment = cls.get(comment_id)
        if not comment:
            return None
        db.session.delete(comment)
        db.session.commit()