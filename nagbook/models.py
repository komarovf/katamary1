import re
from datetime import datetime, timedelta

from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager as lm


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    nickname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.String(100))

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_pass(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        if check_password_hash(self._password, plaintext):
            return True
        return False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return str(self.nickname)


class Survey(db.Model):
    __tablename__ = 'survey'
    id = db.Column(db.Integer, primary_key=True)
    survey_name = db.Column(db.String(128), index=True)
    intro_text = db.Column(db.String(999), index=True)
    start_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questions = db.relationship('Question', lazy="dynamic", backref='survey')
    respondents_emails = db.relationship('Respondent', lazy="dynamic", backref='survey')

    def __repr__(self):
        return '<survey_name %r>' % self.survey_name


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    type = db.Column(db.String(25))
    consecutive_number = db.Column(db.Integer)
    q_object = db.Column(db.PickleType())

    def __repr__(self):
        return '<q_object %r>' % self.q_object


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<answer %r for question %r>' % self.answer, self.question_id


class Respondent(db.Model):
    __tablename__ = 'respondent'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    sent_status = db.Column(db.Boolean())

    def __repr__(self):
        return '<respondent %r>' % self.email
