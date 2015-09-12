from flask import render_template, url_for

from . import auth
from .forms import RegisterForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            nickname=form.nickname.data,
            password=form.password.data,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your successfully registered!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)