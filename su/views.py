# -*- coding:utf-8 -*-
from flask import Blueprint, render_template,request
from su.extensions import db
from su.models import User


fronted = Blueprint('/', __name__,template_folder='templates')

@fronted.route('/create-db')
def create_db():
    db.create_all()
    return u"创建数据库"

@fronted.route('/add-user/')
def user():
     u = User('xiaosuer2', 'admin@163.co2m')
     p = User('sudongdongr', 'admin@163.co3m')
     db.session.add(u)
     db.session.add(p)
     db.session.commit()
     return u"添加用户ok"

@fronted.route('/edit-user/')
def edit_user():
    user = User.query.filter_by(username='xiaosuer').first()
    user.username = u"大坏蛋"
    db.session.add(user)
    db.session.commit()
    return u"修改用户okle"



@fronted.route('/register/',methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        return "%s regist ok" % username
    else:
        return render_template('regist.html')
