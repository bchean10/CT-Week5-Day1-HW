from flask import render_template, request, redirect, url_for
import requests
from app import app
from .forms import PokeForm, LoginForm, RegisterForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokemons', methods=['GET', 'POST'])
def pokemons():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
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
            return render_template("pokemon.html.j2",form=form, pokemon=pokemon_dict)
        else:
            error_string="Please check for error"
            render_template("pokemon.html.j2",form=form, error=error_string)
    return render_template("pokemon.html.j2", form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
                }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            error_string="There was a problem creating your account. Please try again."
            return render_template('register.html.j2', form=form, error=error_string)
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        if u is not None and u.check_hashed_password(password):
            login_user(u)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html.j2", form=form)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        return redirect(url_for('login'))