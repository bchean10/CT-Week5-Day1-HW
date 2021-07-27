from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')


@app.route('/pokemons', methods=['GET', 'POST'])
def pokemons():
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            if not data:
                error_string=f'There is no info for {pokemon_name}'
                return render_template("pokemon.html.j2",error=error_string)
            pokemon_dict={
                'pokemon_name':data['forms'][0]['name'], 
                'abilities':data['abilities'][0]['ability']['name'],
                'base_experience':data['base_experience'],
                'sprites':data['sprites']['front_shiny']
            }
            return render_template("pokemon.html.j2",pokemon=pokemon_dict)
        else:
            error_string="Please check for error"
            render_template("pokemon.html.j2",error=error_string)
    return render_template("pokemon.html.j2")