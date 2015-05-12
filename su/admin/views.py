from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from su.config import Config
admin = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')

@admin.route('/')
@admin.route('/login/')
# def index():
#     return "hello admin blueprint"
@admin.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != Config.USERNAME:
            error = 'Invalid username'
        elif request.form['password'] != Config.PASSWORD:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)

@admin.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('logout'))
