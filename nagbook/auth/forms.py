from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import Required, Length, Email

from ..models import User


class RegisterForm(Form):
    nickname = StringField(
        'nickname',
        validators=[Required()]
    )
    email = StringField(
        'email',
        validators=[
            Required(),
            Email('Please, enter valid email')
        ]
    )
    password = PasswordField(
        'password',
        validators=[
            Required(),
            Length(min=6, message=('Please give a longer password'))
        ]
    )
    confirm_pass = PasswordField(
        'confirm_pass',
        validators=[Required()]
    )

    def validate(self):
        if not Form.validate(self):
            return False

        if self.nickname.data != User.make_valid_login(self.nickname.data):
            self.nickname.errors.append(
                'Please use letters, numbers, dots and underscores only'
            )
            return False

        if self.password.data != self.confirm_pass.data:
            self.confirm_pass.errors.append('Passwords should be identical')
            return False

        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('This nickname is already in use')
            return False

        return True


class LoginForm(Form):
    email = StringField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append('Invalid email or password')
            self.password.errors.append('Invalid email or password')
            return False

        if not user.is_correct_password(self.password.data):
            self.email.errors.append('Invalid email or password')
            self.password.errors.append('Invalid email or password')
            return False

        return True
