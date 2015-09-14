from functools import wraps

from flask import current_app, redirect, flash, url_for
from flask.ext.login import current_user


def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            elif current_user.role not in roles:
                flash('Permission denied!')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
