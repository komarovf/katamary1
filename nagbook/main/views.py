from flask import render_template, url_for

from . import main

from .. import mandrill


@main.route('/')
def index():
    return render_template('main/index.html')