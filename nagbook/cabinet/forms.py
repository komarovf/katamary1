from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email
from ..models import Survey


class EmailAddForm(Form, id):
    email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    submit = SubmitField('Add')

    def validate_email(self, email):
            if email in (Survey.query.filter_by(id=id).first().respondents_emails):
                raise ValidationError('Email already registered.')