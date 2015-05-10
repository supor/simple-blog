#! coding:utf-8

from flask import Flask
from su.config import Config
from su.extensions import db



def create_app():
    # 创建flask app
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)
    # 初始化sqlalchemy
    db.init_app(app)

    # 注册蓝图
    from su.admin.views import admin
    from su.views import home

    app.register_blueprint(home)
    app.register_blueprint(admin)
    return app


