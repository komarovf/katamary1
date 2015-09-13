from flask import render_template, redirect, url_for, flash, request, abort
from flask.ext.login import login_required, current_user
from . import user
from ..models import Survey
#from .forms import AddQuestionForm, AddAnswerForm


@user.route('/<int:id>')
@login_required
def search_for_question(id):
    if current_user.id != id :
        abort(403)
    surveys = Survey.query.filter(Survey.user_id == current_user.id).all() or []
    return render_template('index.html', surveys=surveys, current_user=current_user)