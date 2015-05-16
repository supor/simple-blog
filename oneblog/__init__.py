#! coding:utf-8

from flask import Flask, session, g
from .models import User

_guest = User('guest', 'email', 'password', 'bio', 1, 'guest', id=0)

def create_app():
    # 创建flask app
    app = Flask(__name__)

    # 加载配置
    from .config import Config
    from .extensions import db, markdown
    from .lang import text
    from .helper import siteconfig, categories, menus
    from . import lang

    app.config.from_object(Config)
    db.init_app(app)
    lang.setup(app.config.get('LANGUAGE', 'en_GB'))
    app.jinja_env.globals.update(__=text)
    app.jinja_env.globals.update(site=siteconfig, site_categories=categories, menus=menus)
    app.jinja_env.filters['markdown'] = markdown.convert

    # 注册蓝图
    from .controller import admin_bp, site_bp
    from .views import home
    app.register_blueprint(admin_bp)
    app.register_blueprint(site_bp)
    app.register_blueprint(home)

    # 注册钩子方法
    app.before_request(init_user)

    return app

def init_user():
    """Load user if the auth session validates."""
    try:
        user = _guest
        if 'auth' in session:
            uid = session['auth']
            user = User.query.get(uid)
        if user is None:
            session.pop('auth', None)
            user = _guest
    except:
        user = _guest
    g.user = user
