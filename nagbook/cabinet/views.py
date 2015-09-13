from flask import render_template, abort
from flask.ext.login import login_required, current_user
from . import cabinet
from ..models import Survey


@cabinet.route('/<int:user_id>')
@login_required
def index(user_id):
    if current_user.id != user_id:
        abort(403)
    surveys = Survey.query.filter(Survey.user_id == current_user.id).all() or []
    return render_template('index.html', surveys=surveys, current_user=current_user)

@cabinet.route('/distribution/<int:id>')
@login_required
def distribution(id):
    if current_user.id != Survey.query.filter(Survey.id == id).first().user_id:
        abort(403)

@cabinet.route('/statistic/<int:user_id>')
@login_required
def statistic(user_id):
    if current_user.id != user_id:
        abort(403)