from hashlib import md5

from flask import render_template, abort, g
from flask.ext.login import login_required, current_user
from sqlalchemy import func, and_

from . import cabinet
from ..models import Survey, Respondent
from .. import db


@cabinet.before_request
def before_request():
    g.user = current_user


@cabinet.route('/<int:user_id>')
@login_required
def index(user_id):
    if current_user.id != user_id:
        abort(403)
    surveys = Survey.query.filter(Survey.user_id == current_user.id).all() or []
    return render_template(
        'cabinet/index.html',
        surveys=surveys,
        current_user=current_user
    )


@cabinet.route('/distribution/<int:id>')
@login_required
def distribution(id):
    if current_user.id != Survey.query.filter(Survey.id == id).first().user_id:
        abort(403)
    respondents = Respondent.query.filter(Respondent.survey_id == id).all()
    print respondents
    return render_template(
        'cabinet/distribution.html',
        respondents=respondents,
        survey_id=id,
    )


@cabinet.route('/statistic/<int:user_id>')
@login_required
def statistic(user_id):
    if current_user.id != user_id:
        abort(403)
    survey_ids = [
        a[0] for a in (
            db.session.query(Survey.id)
            .filter(Survey.user_id == current_user.id)
            .all()
        )
    ]
    all_respondents = (
        db.session.query(func.count(Respondent.id))
        .filter(Respondent.survey_id.in_(survey_ids))
        .scalar()
    )
    answered_respondents = (
        db.session.query(func.count(Respondent.id))
        .filter(
            and_(
                Respondent.survey_id.in_(survey_ids),
                Respondent.sent_status
            )
        )
        .scalar()
    )
    percent_of_entered = (
        (float(answered_respondents)/all_respondents)*100
        if all_respondents else 0
    )
    return render_template(
        'cabinet/statistic.html',
        percent_of_entered=percent_of_entered
    )
