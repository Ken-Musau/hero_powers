#!/usr/bin/env python3
from flask_restful import Api, Resource
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

ma = Marshmallow(app)


class PowerSchema(ma.Schema):
    class Meta:
        model = Power
        fields = ("id", "name", "description")


power_schema = PowerSchema()
powers_schema = PowerSchema(many=True)


class HeroSchema(ma.Schema):
    class Meta:
        model = Hero

        fields = ("id", "name", "super_name")


hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)


class HeroPowerSchema(ma.Schema):
    class Meta:
        model = HeroPower
        fields = ("id", "strength", "hero_id", "power_id")


heropower_schema = HeroPowerSchema()
heropowers_schema = HeroPowerSchema(many=True)


class Home(Resource):
    def get(self):
        return make_response("<h1>Welcome to Power Hero API</h1>")


class Heroes(Resource):
    def get(self):
        heroes = [hero for hero in Hero.query.all()]
        return make_response(heroes_schema.dump(heroes), 200)


class HeroesById(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()

        if hero:
            # Fetch hero_powers associated with the hero
            hero_powers = hero.hero_powers

            # Extract power details from hero_powers
            powers = [hero_power.power for hero_power in hero_powers]

            # Serialize the hero along with associated powers
            serialized_hero = hero_schema.dump(hero)
            serialized_hero["powers"] = powers_schema.dump(powers)

            return make_response(jsonify(serialized_hero), 200)

        return make_response({'error': "Hero not found"}, 404)

    def delete(self, id):
        hero = Hero.query.filter_by(id=id).first()

        if hero:
            db.session.delete(hero)
            db.session.commit()
            return make_response(["Hero has been deleted"], 200)
        return make_response(jsonify({"error": "Hero not found"}), 404)


class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        return make_response(powers_schema.dump(powers), 200)

    def post(self):
        data = request.get_json()

        try:
            power = Power(
                name=data.get("name"),
                description=data.get("description")
            )

            db.session.add(power)
            db.session.commit()

            return make_response(power_schema.dump(power), 201)

        except ValueError as e:
            return make_response(jsonify({"message": str(e)}), 400)


class PowerById(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()

        if power:
            return make_response(power_schema.dump(power), 200)
        return make_response({"error": "Power not found"}, 404)

    def patch(self, id):
        power = Power.query.filter_by(id=id).first()
        data = request.get_json()

        for attr, value in data.items():
            setattr(power, attr, value)

        db.session.commit()

        if power:
            return make_response(power_schema.dump(power), 200)

    def delete(self, id):
        power = Power.query.filter_by(id=id).first()
        db.session.delete(power)
        db.session.commit()

        return make_response(["Power Succesfully deleted"], 200)


class HeroPowers(Resource):
    def get(self):
        heroPowers = [heroPower
                      for heroPower in HeroPower.query.all()]
        return make_response(heropowers_schema.dump(heroPowers), 200)

    def post(self):
        data = request.get_json()

        try:

            heroPower = HeroPower(
                strength=data.get("strength"),
                hero_id=data.get("hero_id"),
                power_id=data.get("power_id")

            )
            db.session.add(heroPower)
            db.session.commit()

            hero = Hero.query.filter(Hero.id == heroPower.hero_id).first()

            hero_powers = hero.hero_powers

            powers = [hero_power.power for hero_power in hero_powers]
            serialized_hero = hero_schema.dump(hero)
            serialized_hero["powers"] = powers_schema.dump(powers)

            return make_response(jsonify(serialized_hero), 201)

        except ValueError as e:
            return make_response(jsonify({"message": str(e)}), 400)


class HeroPowerById(Resource):
    def get(self, id):
        heroPower = HeroPower.query.filter_by(id=id).first()

        return make_response(jsonify(heropower_schema.dump(heroPower)), 200)

    def delete(self, id):
        heroPower = HeroPower.query.filter_by(id=id).first()

        if heroPower:
            db.session.delete(heroPower)
            db.session.commit()
            return make_response(["Hero_Power succesful deleted"])
        return make_response(jsonify({"error": "Hero_power not found"}), 404)


api.add_resource(Home, "/")
api.add_resource(Heroes, "/heroes")
api.add_resource(HeroesById, "/heroes/<int:id>")
api.add_resource(Powers, "/powers")
api.add_resource(PowerById, "/powers/<int:id>")
api.add_resource(HeroPowers, "/hero_powers")
api.add_resource(HeroPowerById, "/hero_powers/<int:id>")

if __name__ == '__main__':
    app.run(port=5555)
