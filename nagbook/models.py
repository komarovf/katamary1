import re

from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager as lm


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model):
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
