# -*- coding:utf-8 -*-
class Config():
    DEBUG = True
    SECRET_KEY = 'development key'

    # 你这是错的，mysql没有。db文件
    # mysql://scott:tiger@localhost/mydatabase
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/su_blog'