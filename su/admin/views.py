from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')

@admin.route('/')
@admin.route('/hello/')
def index():
    return "hello admin blueprint"