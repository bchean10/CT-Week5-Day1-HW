from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login


# new_pokemon = db.Table('new_pokemon', db.Column('pokemon_id', db.Integer, db.ForeignKey('pokedata.id')), 
#     db.Column('existing_pokemon_id', db.Integer, db.ForeignKey('pokedata.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    # existing = db.relationship()
    
    
    # def created(self, user):
    #     pass
    
    # def create(self, user):
    #     pass

    # def uncreate(self, user):
    #     pass

    def ___repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.save()

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self) 
        db.session.commit() 

    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

    ## need make changes here