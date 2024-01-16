#!/usr/bin/env python3

from os import environ, path

from dotenv import load_dotenv
from flask import Flask, make_response, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Mission, Planet, Scientist, db

BASE_DIR = path.abspath(path.dirname(__file__))
DATABASE = environ.get(
    "DB_URI", f"sqlite:///{path.join(BASE_DIR, 'app.db')}")

load_dotenv('.env')


app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

@app.route('/set_red')
def set_red():
    res = make_response({"message": "cookie color set to red"}, 200)
    res.set_cookie("color", "red")
    return res

@app.route('/set_num/<int:num>')
def set_num(num):
    res = make_response({"message": f"num set to {num}"}, 200)
    res.set_cookie("num", str(num))
    return res

@app.route('/current_color')
def current_color():
    return make_response({"color": request.cookies.get("color")}, 200)


@app.route('/sign_in', methods=("POST","GET"))
def sign_in():
    # data = request.get_json()
    #user = User.query.filter_by(username=data.get('username'))
    
    # check if password from data matches password of user
    
    # res = make_response({"message": f"signed in as user {user.id}"}, 200)
    
    session["user_id"] = 1
    return make_response({"message": f"signed in as user {session.get('user_id')}"}, 200)

@app.route('/check_session')
def check_session():
    return make_response({"user_id": session.get("user_id")}, 200)


class Scientists(Resource):
    def get(self):
        return make_response([scientist.to_dict() for scientist in Scientist.query.all()], 200)
    
    def post(self):
        data = request.get_json()
        scientist = Scientist()
        try:
            scientist.name = data.get("name")
            scientist.field_of_study = data.get("field_of_study")
            db.session.add(scientist)
            db.session.commit()
            return make_response(scientist.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
    
api.add_resource(Scientists, '/scientists')

class ScientistById(Resource):
    def get(self, id):
        scientist = Scientist.query.get(id)
        if not scientist:
            return make_response({"error": "Scientist not found"}, 404)
        return make_response(scientist.to_dict(rules=("missions", "missions.planet")), 200)
    
    def patch(self, id):
        scientist = Scientist.query.get(id)
        if not scientist:
            return make_response({"error": "Scientist not found"}, 404)
        data = request.get_json()
        try:
            for attr in data:
                setattr(scientist, attr, data[attr])
                
            db.session.add(scientist)
            db.session.commit()
            return make_response(scientist.to_dict(), 202)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
        
    def delete(self, id):
        scientist = Scientist.query.get(id)
        if not scientist:
            return make_response({"error": "Scientist not found"}, 404)
        db.session.delete(scientist)
        db.session.commit()
        return make_response({}, 204)
    
api.add_resource(ScientistById, '/scientists/<int:id>')

class Planets(Resource):
    def get(self):
        return make_response([planet.to_dict() for planet in Planet.query.all()], 200)
    
api.add_resource(Planets, "/planets")

class Missions(Resource):
    def post(self):
        data = request.get_json()
        mission = Mission()
        try:
            mission.name = data.get("name")
            mission.planet_id = data.get("planet_id")
            mission.scientist_id = data.get("scientist_id")
            db.session.add(mission)
            db.session.commit()
            return make_response(mission.to_dict(rules=("planet", "scientist")), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
    
api.add_resource(Missions, "/missions")


if __name__ == '__main__':
    app.run(port=5555, debug=True)
