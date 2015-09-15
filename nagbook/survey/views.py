from hashlib import md5
from datetime import datetime

from flask import render_template, abort, g, request, jsonify
from flask.ext.login import login_required, current_user

from . import survey
from .. import db, mandrill
from ..models import Survey, Question, Respondent, Answer


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
    db.session.flush()
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
        hash = str(survey.id) + "_" + md5(respondent_json).hexdigest()

        # mandrill.send_email(
        #    from_email='komarovf88@gmail.com',
        #    to=[{'email': respondent_json}],
        #    text='1337'
        # )

    db.session.commit()
    return jsonify({"status": "ok"})


@survey.route('/answer/<hash>', methods=['GET', 'POST'])
def add_answer(hash):
    survey_id, email_hash = hash.split('_')
    survey_id = int(survey_id)

    hashes = map(
        lambda r: md5(r.email_hash).hexdigest(),
        Respondent.query.filter_by(survey_id=survey_id).all()
    )
    if email_hash not in hashes:
        abort(404)

    survey = Survey.query.get(survey_id)

    if request.method == 'POST':
        # Save Answers here
        answers = request.json
        for i, q in enumerate(survey.questions.all()):
            a = Answer(
                email=email_hash,
                question_id=q.id,
                answer=answers[str(i)]
            )
            db.session.add(a)
        db.session.commit()
        return jsonify({"status": "ok"})

    return render_template('survey/answer_form.html', survey_id=survey_id)


@survey.route('/get/<int:survey_id>', methods=['GET'])
def get_survey(survey_id):
    result = {}
    survey = Survey.query.get(survey_id)
    result["name"] = survey.name
    result["intro_text"] = survey.intro_text
    result["start_time"] = survey.start_time
    result["end_time"] = survey.end_time
    result["questions"] = (
        list(map(
            lambda x: dict(
                body=x.body,
                type=x.type,
                answers=x.q_object
            ),
            survey.questions.all()
        ))
    )
    return jsonify(survey=result)
