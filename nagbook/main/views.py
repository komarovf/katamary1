from flask import render_template, url_for, g

from flask.ext.login import current_user, login_required

from . import main
from .. import login_manager as lm
from ..models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.before_request
def before_request():
    g.user = current_user

from .. import mandrill


@main.route('/')
def index():
    return render_template('main/index.html')