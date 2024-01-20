#!/usr/bin/env python3

from config import app, db, api
from flask import make_response, request, session

from flask_restful import Resource
from models import Mission, Planet, Scientist, User
from sqlalchemy.exc import IntegrityError

@app.route('/')
def home():
    return ''

@app.route('/sign_up', methods=("POST",))
def sign_up():
    data = request.get_json()
    
    try:
        user = User(username=data.get("username"), password_hash=data.get("password"))
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        
        return make_response(user.to_dict(), 201)
        
    except ValueError as e:
        return make_response({"error": e.__str__()}, 400)
    except IntegrityError:
        return make_response({"error": "Database constraint error"}, 400)

@app.route('/sign_in', methods=("POST",))
def sign_in():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user:
        if user.authenticate(data.get("password")):
            session["user_id"] = user.id
            return make_response(user.to_dict(), 200)
    session.clear()
    return make_response({"error": "Incorrect username or password"}, 401)


@app.route('/sign_out', methods=("DELETE",))
def sign_out():
    session.clear()
    return make_response({}, 204)

@app.route('/check_session')
def check_session():
    user = User.query.get(session.get("user_id"))
    if user:
        return make_response(user.to_dict(), 200)
    else:
        return make_response({}, 401)


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
