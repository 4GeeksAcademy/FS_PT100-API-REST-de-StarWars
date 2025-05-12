"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Vehicle, Planet, FavoritePeople, FavoritePlanet
from sqlalchemy import select

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    return jsonify({"msg": "Hello, this is your GET /user response"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

####### USER #######
@app.route("/users", methods=["GET"])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    return jsonify([user.serialize() for user in users]), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_user = User(email=data["email"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user = db.session.execute(select(User).where(User.id == id)).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = db.session.execute(select(User).where(User.id == id)).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

####### PEOPLE #######
@app.route("/people", methods=["GET"])
def get_people_list():
    people = db.session.execute(select(People)).scalars().all()
    return jsonify([p.serialize() for p in people]), 200

@app.route("/people/<int:people_id>", methods=["GET"])
def get_people(people_id):
    person = db.session.execute(select(People).where(People.id == people_id)).scalar_one_or_none()
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

@app.route("/people", methods=["POST"])
def create_people():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_person = People(name=data["name"])
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

@app.route("/people/<int:id>", methods=["PUT"])
def update_people(id):
    data = request.get_json()
    person = db.session.execute(select(People).where(People.id == id)).scalar_one_or_none()
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    person.name = data.get("name", person.name)
    db.session.commit()
    return jsonify(person.serialize()), 200

@app.route("/people/<int:id>", methods=["DELETE"])
def delete_people(id):
    person = db.session.execute(select(People).where(People.id == id)).scalar_one_or_none()
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "Person deleted"}), 200

####### VEHICLE #######
@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    vehicles = db.session.execute(select(Vehicle)).scalars().all()
    return jsonify([v.serialize() for v in vehicles]), 200

@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    vehicle = db.session.execute(select(Vehicle).where(Vehicle.id == vehicle_id)).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

@app.route("/vehicles", methods=["POST"])
def create_vehicle():
    data = request.get_json()
    if not data or "name" not in data or "model" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_vehicle = Vehicle(name=data["name"], model=data["model"])
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.serialize()), 201

@app.route("/vehicles/<int:id>", methods=["PUT"])
def update_vehicle(id):
    data = request.get_json()
    vehicle = db.session.execute(select(Vehicle).where(Vehicle.id == id)).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    vehicle.name = data.get("name", vehicle.name)
    vehicle.model = data.get("model", vehicle.model)
    db.session.commit()
    return jsonify(vehicle.serialize()), 200

@app.route("/vehicles/<int:id>", methods=["DELETE"])
def delete_vehicle(id):
    vehicle = db.session.execute(select(Vehicle).where(Vehicle.id == id)).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted"}), 200

####### PLANET #######
@app.route("/planets", methods=["GET"])
def get_planets():
    planets = db.session.execute(select(Planet)).scalars().all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = db.session.execute(select(Planet).where(Planet.id == planet_id)).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route("/planets", methods=["POST"])
def create_planet():
    data = request.get_json()
    if not data or "name" not in data or "model" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_planet = Planet(name=data["name"], model=data["model"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route("/planets/<int:id>", methods=["PUT"])
def update_planet(id):
    data = request.get_json()
    planet = db.session.execute(select(Planet).where(Planet.id == id)).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    planet.name = data.get("name", planet.name)
    planet.model = data.get("model", planet.model)
    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route("/planets/<int:id>", methods=["DELETE"])
def delete_planet(id):
    planet = db.session.execute(select(Planet).where(Planet.id == id)).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": "Planet deleted"}), 200

####### FAVORITE PLANET #######
@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    new_fav = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    fav = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 204

####### FAVORITE PEOPLE #######
@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    new_fav = FavoritePeople(user_id=user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    user_id = request.json.get("user_id")
    fav = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not fav:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 204