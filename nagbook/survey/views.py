from flask import render_template, abort, g, request
from flask.ext.login import login_required, current_user
from . import survey
from ..models import Survey


@survey.before_request
def before_request():
    g.user = current_user


@survey.route('/<int:user_id>', methods=['GET'])
@login_required
def show_add_form(user_id):
    if current_user.id != user_id:
        abort(403)
    return render_template('survey/add_form.html')


@survey.route('/<int:user_id>', methods=['POST'])
@login_required
def add(user_id):
    if current_user.id != user_id:
        abort(403)
    print request.json
    return 0
