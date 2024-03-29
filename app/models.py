from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
# from sqlalchemy.schema import CheckConstraint


db = SQLAlchemy()


class Hero(db.Model):
    __tablename__ = 'heroes'

    # serialize_rules = ("-hero_powers.hero",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    # hero_powers = db.relationship("HeroPower", backref="hero")

    hero_powers = db.relationship(
        "HeroPower", back_populates="hero", cascade="all, delete-orphan")


class HeroPower(db.Model):
    __tablename__ = "hero_powers"

    # serialize_rules = ("-power.hero_powers", "-hero.hero_powers",)

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"))

    power = db.relationship("Power", back_populates="hero_powers")
    hero = db.relationship("Hero", back_populates="hero_powers")

    @validates("strength")
    def validate_strength(self, key, strength):
        strength_value = ['Strong', 'Weak', 'Average']
        if strength not in strength_value:
            raise ValueError("Strength must be either Strong, Weak, Average")
        return strength


class Power(db.Model):
    __tablename__ = "powers"

    # serialize_rules = ("-hero_powers.power",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String,  nullable=False)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), onupdate=db.func.now())

    @validates("description")
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be more than 20 characters")
        return description

    # hero_powers = db.relationship("HeroPower", backref="power")

    hero_powers = db.relationship(
        "HeroPower", back_populates="power", cascade="all, delete-orphan")
