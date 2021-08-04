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
