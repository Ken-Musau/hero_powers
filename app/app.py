#!/usr/bin/env python3
from flask_restful import Api, Resource
from flask import Flask, jsonify, make_response
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


class HeroWithPowersSchema(ma.Schema):
    class Meta:
        model = Hero
        fields = ("id", "name", "super_name", "powers")

    powers = ma.Nested("PowerSchema", many=True, only=(
        "id", "name"), attribute="hero_powers")


hero_with_powers_schema = HeroWithPowersSchema()
heroes_with_powers_schema = HeroWithPowersSchema(many=True)


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
            return make_response(hero_with_powers_schema.dump(hero), 200)
        return make_response({'error': "Hero not found"})


class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        return make_response(powers_schema.dump(powers), 200)


class powerById(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()

        if power:
            return make_response(power_schema.dump(power), 200)
        return make_response({"error": "Power not found"}, 404)


class HeroPowers(Resource):
    def get(self):
        heroPowers = [heroPower
                      for heroPower in HeroPower.query.all()]
        return make_response(heropowers_schema.dump(heroPowers), 200)


class HeroPowerById(Resource):
    def get(self, id):
        heroPower = HeroPower.query.filter_by(id=id).first()

        return make_response(jsonify(heroPower.to_dict()), 200)


api.add_resource(Home, "/")
api.add_resource(Heroes, "/heroes")
api.add_resource(HeroesById, "/heroes/<int:id>")
api.add_resource(Powers, "/powers")
api.add_resource(powerById, "/powers/<int:id>")
api.add_resource(HeroPowers, "/hero_powers")
api.add_resource(HeroPowerById, "/hero_powers/<int:id>")

if __name__ == '__main__':
    app.run(port=5555)
