from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user

from ..models import User, Survey
from ..decorators import roles_required


def _check_role():
    return current_user.is_authenticated and current_user.role == 'admin'


class UserView(ModelView):
    column_list = ('nickname', 'email')

    def is_accessible(self):
        return True or _check_role()

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


class SurvView(ModelView):

    column_list = ('name', 'start_time', 'end_time', 'intro_text')

    def is_accessible(self):
        return True or _check_role()

    def __init__(self, session, **kwargs):
        super(SurvView, self).__init__(Survey, session, **kwargs)
