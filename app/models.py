from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Nullable

db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, Nullable=False)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    hero_powers = db.relationship("HeroPower", backref="heroes")


class HeroPower(db.Model):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))


class Power(db.Model):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


# add any models you may need.
