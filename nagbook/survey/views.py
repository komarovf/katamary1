from hashlib import md5
from datetime import datetime

from flask import render_template, abort, g, request, jsonify, url_for
from flask.ext.login import login_required, current_user

from . import survey
from .. import db, mandrill
from ..models import Survey, Question, Respondent, Answer
from ..decorators import async_email_send


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
        url = url_for('survey.add_answer', hash=hash, _external=True)
        email_text = """
        <html>
            <head></head>
            <body>
                <h1>You invited for survey: {0}</h1>
                <a href="{1}">Go to survey page!</a>
            </body>
        </html>
        """.format(survey.name, url)

        # Non blocking emails send
        mandrill.send_email = async_email_send(mandrill.send_email)
        mandrill.send_email(
            html=email_text,
            text=url,
            subject="Survey invitation!",
            from_email='noreply@survey.com',
            to=[{'email': respondent_json}],
            async=True
        )

    db.session.commit()
    return jsonify({"status": "ok"})


@survey.route('/answer/<hash>', methods=['GET', 'POST'])
def add_answer(hash):
    if "_" in hash:
        survey_id, email_hash = hash.split('_')
    else:
        abort(404)

    survey_id = int(survey_id)

    hashes = dict(map(
        lambda r: (md5(r.email_hash).hexdigest(), r.id),
        Respondent.query.filter_by(survey_id=survey_id).all()
    ))

    # Change this after making all survays public (integration on public pages)
    if email_hash not in hashes.keys():
        abort(404)
    else:
        respondent = Respondent.query.get(hashes[email_hash])

    # prevent double submission
    if respondent.sent_status:
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
        respondent.sent_status = True
        db.session.add(respondent)
        db.session.commit()
        return jsonify({"status": "ok"})

    return render_template('survey/answer_form.html', survey_id=survey_id)


@survey.route('/analize/<email>/<int:id>', methods=['GET'])
@login_required
def analize_answer(email, id):
    hash = md5(email).hexdigest()
    survey = Survey.query.get(id)
    questions = survey.questions.all()
    answers = (
        Answer.query
        .filter_by(email=hash)
        .filter(Answer.question_id.in_(map(lambda x: x.id, questions)))
        .all()
    )
    return render_template(
        'survey/results.html',
        questions=questions,
        answers=answers,
        survey=survey
    )


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
