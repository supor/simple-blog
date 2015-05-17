# -*- coding: utf-8 -*-
'''
Created on 2015-5-16

@author: Nob
'''
import re
from datetime import datetime
from flask import session, g
from .lib.paginator import Paginator
from .helper import siteconfig
from .extensions import db
from .models import User, Post, Category, Comment, Page
from _ast import keyword

class UserService(object):
    @staticmethod
    def auth(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.active() and user.check(password):
            return user
        return False

    @staticmethod
    def login(user):
        session.permanent = True
        session['auth'] = user.id

    @staticmethod
    def logout():
        session.pop('auth', None)

    @staticmethod
    def get(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def page(page, perpage=5):
        total = User.query.count()
        users = User.query.paginate(page, perpage, error_out=False).items
        pagination = Paginator(users, total, page, perpage, '/admin/user')
        return pagination

    @staticmethod
    def get_user_page(user):
        return Paginator([user], 1, 1, 5, '/admin/user')

    @staticmethod
    def add_user(username, email, password, bio, status, role):
        user = User(username, email, password, bio, status, role)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def update_user(cls, uid, email, newpass1, bio, status, role):
        user = cls.get(uid)
        if not user:
            return None
        user.email = email
        user.password = newpass1
        user.bio = bio
        user.status = status
        user.role = role
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def delete(cls, user_id):
        user = cls.get(user_id)
        if not user:
            return None
        db.session.delete(user_id)
        db.session.commit()

class PostService(object):
    @staticmethod
    def get_by_pid(id):
        return Post.query.filter_by(id=id).first()

    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(slug=slug).first()

    @staticmethod
    def search(keyword, page, perpage=10):
        q = Post.query.filter(Post.slug.like('%'+ keyword +'%')).filter(Post.title.like('%'+ keyword +'%'))
        total = q.count()
        posts = q.paginate(page, perpage, error_out=False).items
        pagination = Paginator(posts, total, page, perpage, '/admin/post')
        return pagination

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
        post.create_time = datetime.now()
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
    def get(id):
        return Category.query.filter_by(id=id).first()

    @staticmethod
    def dropdown():
        """Returns the all category id"""
        return Category.query.all()

    @staticmethod
    def page(page=1, perpage=10):
        total = Category.query.count()
        categories = Category.query.paginate(page, perpage, error_out=False).items
        pagination = Paginator(categories, total, page, perpage, '/admin/category')
        return pagination

    @staticmethod
    def add_category(title, slug, description, sort=1):
        category = Category(title, slug, description, sort)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def update_category(cls, category_id, title, slug, description, sort=1):
        category = cls.get(category_id)
        if not category:
            return None
        category.slug = slug or title
        category.title = title
        category.description = description
        category.sort = sort
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def delete(cls, category_id):
        category = cls.get(category_id)
        if not category:
            return None
        db.session.delete(category)
        db.session.commit()

class CommentService(object):
    @staticmethod
    def get(id):
        return Comment.query.filter_by(id=id).first()

    @staticmethod
    def page(status, page=1, perpage=10):
        q = Comment.query
        if status and status != 'all':
            q = q.filter_by(status=status)
        total = q.count()
        comments = q.paginate(page, perpage, error_out=False).items
        pagination = Paginator(comments, total, page, perpage, '/admin/comment')
        return pagination

    @classmethod
    def add_comment(cls, name, email, content, status, post):
        comment = Comment(post.id, name, email, content, status)
        if cls.is_spam(comment):
            comment.status = 'spam'
        db.session.add(comment)
        db.session.commit()
        return comment

    @classmethod
    def is_spam(cls, comment):
        for word in siteconfig.comment_moderation_keys():
            if word.strip() and re.match(word, comment.content, re.I):
                return True
        domain = comment.email.split('@')[1]
        if cls.spam_count(domain):
            return True
        return False

    @classmethod
    def spam_count(self, domain):
        """ 根据已经加黑的邮箱同域名判断垃圾评论数量 """
        return Comment.query.filter(Comment.email.like('%'+ domain +'%')).count()

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

class PageService(object):
    @staticmethod
    def get(id):
        return Page.query.filter_by(id=id).first()

    @staticmethod
    def page(status, page=1, perpage=10):
        q = Page.query
        if status and status != 'all':
            q = q.filter_by(status=status)
            url = '/admin/page/status/' + status
        else:
            url = '/admin/page'
        total = q.count()
        pages = q.paginate(page, perpage, error_out=False).items
        pagination = Paginator(pages, total, page, perpage, url)
        return pagination

    @staticmethod
    def get_published_posts_page(page=1, perpage=10, category_id=None):
        cid = None
        if category_id:
            category = Category.query.filter_by(slug=category_id).first()
            if not category:
                return Paginator([], 0, page, perpage, '/category/' + category_id)
            cid = category.id
        q = Post.query
        if cid:
            q = q.filter_by(category_id=cid)
        total = q.count()
        posts = q.paginate(page, perpage, error_out=False).items
        url = 'category/' + category_id if category_id else '/posts'
        pagination = Paginator(posts, total, page, perpage, url)
        return total, pagination

    @staticmethod
    def dropdown(show_empty_option=True, show_in_menu=1, exclude=[]):
        """Returns the all page id"""
        items = []
        if show_empty_option:
            empty_page = Page('--', 'title', 'slug', 'content')
            empty_page.id = 0
            items.append(empty_page)
        pages = Page.query.filter_by(show_in_menu=show_in_menu).all()
        for page in pages:
            if page.id in exclude:
                continue
            items.append(page)
        return items

    @staticmethod
    def get_by_slug(slug):
        return Page.query.filter_by(slug=slug).first()

    @staticmethod
    def add_page(parent_id, name, title, slug, content, status, redirect, show_in_menu):
        redirect = redirect.strip()
        show_in_menu = 1 if show_in_menu else 0
        page = Page(name, title, slug, content, status, redirect, show_in_menu, parent_id)
        db.session.add(page)
        db.session.commit()
        return page

    @classmethod
    def update_page(cls, page_id, name, title, slug, content, status, redirect, show_in_menu, parent_id):
        page = cls.get(page_id)
        if not page:
            return None
        show_in_menu = 1 if show_in_menu else 0
        redirect = redirect.strip()
        page.name = name
        page.title = title
        page.slug = slug
        page.content = content
        page.status = status
        page.redirect = redirect
        page.show_in_menu = show_in_menu
        page.parent_id =parent_id
        db.session.add(page)
        db.session.commit()
        return page

    @staticmethod
    def is_exist_slug(slug):
        count = Page.query.filter_by(slug=slug).count()
        return count > 0

    @classmethod
    def delete(cls, page_id):
        page = cls.get(page_id)
        if not page:
            return None
        db.session.delete(page)
        db.session.commit()












