from flask import g
from flask.ext.login import current_user

from . import admin


@admin.before_request
def before_request():
    g.user = current_user
