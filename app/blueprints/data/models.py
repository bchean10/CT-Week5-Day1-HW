from app import db
from datetime import datetime as dt

class PokeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String(150))
    abilities = db.Column(db.String(150))
    base_experience = db.Column(db.Integer)
    sprites = db.Column(db.String())
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow)
    comments = db.relationship('Comment', cascade='all, delete-orphan', backref='pokemon',lazy=True)

    def __repr__(self):
        return f'<id: {self.id} | Pokemon Name: {self.pokemon_name} | Abilities: {self.abilities} | BaseExperience: {self.base_experience} | Sprites:{self.sprites}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, pokemon_name, abilities, base_experience, sprites):
        self.pokemon_name = pokemon_name
        self.abilities = abilities
        self.base_experience = base_experience
        self.sprites = sprites
        self.save()
# 
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    pokemon_id = db.Column(db.Integer(), db.ForeignKey("poke_data.id"))
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    person = db.relationship('User', backref='user',lazy=True, viewonly=True)



    def __repr__(self):
        return f'<id: {self.id} | Body: {self.body[::30]}>'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, body):
        self.body = body
        self.save()
        