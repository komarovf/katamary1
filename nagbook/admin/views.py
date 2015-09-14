from flask import g, render_template
from flask.ext.login import current_user

from . import admin
from ..decorators import roles_required


@admin.before_request
def before_request():
    g.user = current_user


@admin.route('/', methods=['GET'])
@roles_required('admin')
def index():
    return render_template('admin/index.html')
