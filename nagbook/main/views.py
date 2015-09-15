from flask import render_template, url_for, g
from flask.ext.login import current_user, login_required

from ..auth import auth
from . import main
from ..models import User
from .. import mandrill


@main.before_request
def before_request():
    g.user = current_user


@main.route('/')
def index():
    return render_template('main/index.html')
