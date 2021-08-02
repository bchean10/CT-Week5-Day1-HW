from flask import render_template, request, flash
import requests
from flask_login import login_required
from .forms import PokeForm
from . import bp as main

@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/pokemons', methods=['GET', 'POST'])
@login_required
def pokemons():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name = request.form.get('pokemon_name').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            if not data:
                flash(f'There is no info for {pokemon_name}', 'warning')
                return render_template("pokemon.html.j2")
            pokemon_dict={
                'pokemon_name':data['forms'][0]['name'], 
                'abilities':data['abilities'][0]['ability']['name'],
                'base_experience':data['base_experience'],
                'sprites':data['sprites']['front_shiny']
            }
            return render_template("pokemon.html.j2",form=form, pokemon=pokemon_dict)
        else:
            flash(f'Please check for error', 'danger')
            render_template("pokemon.html.j2",form=form)
    return render_template("pokemon.html.j2", form=form)