from flask import render_template
from flask_login import login_required, current_user
from . import bp as data

@data.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@data.route('/pokedata')
@login_required
def pokedata():
    return render_template('poke_data.html.j2')