# -*- coding:utf-8 -*-
class Config():
    DEBUG = True
    SECRET_KEY = 'development key'
    USERNAME='admin'
    PASSWORD='default'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:yiqiwanshua@localhost:3306/su_blog'