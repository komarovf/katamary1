from flask import render_template, url_for, g, session, redirect, flash, request
from flask.ext.login import login_user, logout_user, current_user

from . import auth
from .forms import RegisterForm, LoginForm
from .. import db
from ..models import User


@auth.before_request
def before_request():
    g.user = current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        session['remember_me'] = form.remember_me.data
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        flash('Logged in successfully')
        return redirect(
            request.args.get('next') or
            url_for('cabinet.index', user_id=user.id)
        )
    return render_template('auth/login.html', form=form)


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
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
