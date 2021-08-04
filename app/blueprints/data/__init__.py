from flask import Blueprint

bp = Blueprint('data', __name__, url_prefix='')

from . import routes