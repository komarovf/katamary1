from flask import render_template, abort, g, request, jsonify
from flask.ext.login import login_required, current_user
from datetime import datetime
from . import survey
from .. import db, mandrill
from ..models import Survey, Question, Respondent


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
    data = request.json['data'][0]
    survey = Survey(
        name=data['name'],
        intro_text=data['intro_text'],
        start_time=datetime.strptime(data['start_time'], '%Y-%m-%d'),
        end_time=datetime.strptime(data['end_time'], '%Y-%m-%d'),
        user_id=current_user.id
    )
    db.session.add(survey)
    db.session.commit()
    for i, question_json in enumerate(data['questions']):
        question = Question(
            body=question_json['body'],
            type=question_json['type'],
            survey_id=survey.id,
            consecutive_number=i,
            q_object=question_json['answers'],
        )
        db.session.add(question)
    for respondent_json in data['emails']:
        respondent = Respondent(
            email=respondent_json,
            survey_id=survey.id,
            email_hash=respondent_json,
        )
        db.session.add(respondent)
        #mandrill.send_email(
        #    from_email='komarovf88@gmail.com',
        #    to=[{'email': respondent_json}],
        #    text='1337'
        #)

    return jsonify({"status": "ok"})
