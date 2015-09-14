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
    survey = Survey(
        name=request.json['data'][0]['name'],
        intro_text=request.json['data'][0]['intro_text'],
        start_time=datetime.strptime(request.json['data'][0]['start_time'], '%Y-%m-%d'),
        end_time=datetime.strptime(request.json['data'][0]['end_time'], '%Y-%m-%d'),
        user_id=current_user.id
    )
    db.session.add(survey)
    db.session.commit()
    for question_json in request.json['data'][0]['questions']:
        i=0
        question = Question(
            body=question_json['body'],
            type=question_json['type'],
            survey_id=survey.id,
            consecutive_number=i,
            q_object=question_json['answers'],
        )
        ++i
        db.session.add(question)
    for respondent_json in request.json['data'][0]['emails']:
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
