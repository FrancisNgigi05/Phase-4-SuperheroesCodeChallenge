#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes')
def get_heroes():
    data = []
    heroes = Hero.query.all()

    for hero in heroes:
        hero_dict = hero.less_dict()
        data.append(hero_dict)

    response = make_response(data, 200)

    return response

@app.route('/heroes/<int:id>')
def get_specific_hero(id):
    specific_hero = Hero.query.filter(Hero.id == id).first()

    if not specific_hero:
        response_body = {'error': 'Hero not found'}
        response = make_response(response_body, 404)

        return response
    else:
        data = specific_hero.to_dict()

        response = make_response(data, 200)

        return response
    
@app.route('/powers')
def get_powers():
    data = []

    powers = Power.query.all()

    for power in powers:
        power_dict = power.less_dict()
        data.append(power_dict)

    response = make_response(data, 200)

    return response

@app.route('/powers/<int:id>', methods=['GET', 'PUT'])
def get_specific_power(id):
    specific_power = Power.query.filter(Power.id == id).first()


    if request.method == 'GET':
        if specific_power:

            data = specific_power.less_dict()

            response = make_response(data, 200)

            return response
        else:
            response_body = {'error':'Power not found'}

            response = make_response(response_body, 404)

            return response
    # elif request.method == 'PUT':
    #     if specific_power is None:
    #         response_body = {'error': 'Power not found'}
    #         response = make_response(response_body, 404)
    #         return response
        
    #     elif specific_power is not None:
    #         data = response.json
            
    #         specific_power.name = data.get('name', specific_power.name)
    #         specific_power.description = data.get('description', specific_power.description)

    #         db.session.commit()
    #         return jsonify(specific_power.serialize()), 200
        
    #     else:
    #         return jsonify({'error': ['validation error']})


        
@app.route('/hero_powers', methods=['POST'])
def hero_power():
    data = request.get_json()

    new_hero_power = HeroPower(
        strength=data['strength'],
        power_id=data['power_id'],
        hero_id=data['hero_id']
    )

    db.session.add(new_hero_power)
    db.session.commit()

    new_hero_power_dict = new_hero_power.to_dict()

    response = make_response(new_hero_power_dict, 200)

    return response



if __name__ == '__main__':
    app.run(port=5000, debug=True)

