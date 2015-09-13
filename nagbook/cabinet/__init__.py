from flask import Blueprint

cabinet = Blueprint('cabinet', __name__)

from . import views, forms