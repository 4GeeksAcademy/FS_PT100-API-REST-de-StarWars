"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Vehicle, Planet, FavoritePeople, FavoritePlanet
from sqlalchemy import select
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


####### USER #######
@app.route("/users", methods=["GET"])
def get_users():
    stmt = select(User)
    users = db.session.execute(stmt).scalars().all()
    return jsonify([user.serialize() for user in users]), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    stmt = select(User).where(User.id == user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_user = User(
        email=data["email"],
        password=data["password"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    stmt = select(User).where(User.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user.email = data.get("email", user.email)
    user.password = data.get("password", user.password)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    stmt = select(User).where(User.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

####### People #######
@app.route("/peoples/", methods=["GET"])
def get_peoples():
    stmt = select(People)
    peoples = db.session.execute(stmt).scalars().all()
    return jsonify([people.serialize() for people in peoples]), 200

@app.route("/peoples/<int:people_id>", methods=["GET"])
def get_people(people_id):
    stmt = select(People).where(People.id == people_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route("/peoples", methods=["POST"])
def create_people():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_people = People(
        email=data["email"],
        password=data["password"],
    )
    db.session.add(new_people)
    db.session.commit()
    return jsonify(new_people.serialize()), 201

@app.route("/peoples/<int:id>", methods=["PUT"])
def update_people(id):
    data = request.get_json()
    stmt = select(People).where(People.id == id)
    people = db.session.execute(stmt).scalar_one_or_none()
    if people is None:
        return jsonify({"error": "User not found"}), 404
    people.email = data.get("email", people.email)
    people.password = data.get("password", people.password)
    db.session.commit()
    return jsonify(people.serialize()), 200

@app.route("/peoples/<int:id>", methods=["DELETE"])
def delete_people(id):
    stmt = select(People).where(People.id == id)
    people = db.session.execute(stmt).scalar_one_or_none()
    if people is None:
        return jsonify({"error": "People not found"}), 404
    db.session.delete(people)
    db.session.commit()
    return jsonify({"message": "People deleted"}), 200

####### Vehicle #######
@app.route("/vehicles/", methods=["GET"])
def get_vehicles():
    stmt = select(Vehicle)
    vehicles = db.session.execute(stmt).scalars().all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200

@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    stmt = select(Vehicle).where(Vehicle.id == vehicle_id)
    vehicle = db.session.execute(stmt).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(vehicle.serialize()), 200

@app.route("/vehicles", methods=["POST"])
def create_vehicle():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_vehicle = Vehicle(
        email=data["email"],
        password=data["password"],
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.serialize()), 201

@app.route("/vehicles/<int:id>", methods=["PUT"])
def update_vehicle(id):
    data = request.get_json()
    stmt = select(Vehicle).where(Vehicle.id == id)
    vehicle = db.session.execute(stmt).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    vehicle.email = data.get("email", vehicle.email)
    vehicle.password = data.get("password", vehicle.password)
    db.session.commit()
    return jsonify(vehicle.serialize()), 200

@app.route("/vehicles/<int:id>", methods=["DELETE"])
def delete_vehicle(id):
    stmt = select(Vehicle).where(Vehicle.id == id)
    vehicle = db.session.execute(stmt).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "vehicle not found"}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "vehicle deleted"}), 200

####### Planet #######
@app.route("/planets/", methods=["GET"])
def get_planets():
    stmt = select(Planet)
    planets = db.session.execute(stmt).scalars().all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    stmt = select(Planet).where(Planet.id == planet_id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route("/users", methods=["POST"])
def create_planet():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_planet = Planet(
        email=data["email"],
        password=data["password"],
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route("/planets/<int:id>", methods=["PUT"])
def update_planet(id):
    data = request.get_json()
    stmt = select(Planet).where(Planet.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    planet.email = data.get("email", planet.email)
    planet.password = data.get("password", planet.password)
    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route("/planets/<int:id>", methods=["DELETE"])
def delete_planet(id):
    stmt = select(Planet).where(Planet.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "planet not found"}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": "planet deleted"}), 200

####### Favorite/Planet #######
@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    planet_id = request.json.get("user_id")
    new_fav = FavoritePlanet(planet_id = planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

@app.route("/favorite/planet/<int:id>", methods=["PUT"])
def update_planet(id):
    data = request.get_json()
    stmt = select(Planet).where(Planet.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    planet.email = data.get("email", planet.email)
    planet.password = data.get("password", planet.password)
    db.session.commit()
    return jsonify(planet.serialize()), 200
    
@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    planet_id = request.json.get("user_id")
    fav = FavoritePlanet.query.filter_by(planet_id = planet_id).first()
    if not fav:
        return ("Not found", 404)
    db.session.delete(fav)
    db.session.commit()
    return ("Deleted", 204)

####### Favorite/People #######
@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    people_id = request.json.get("people_id")
    new_fav = FavoritePeople(people_id = people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201

@app.route("/planets/<int:id>", methods=["PUT"])
def update_planet(id):
    data = request.get_json()
    stmt = select(Planet).where(Planet.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    planet.email = data.get("email", planet.email)
    planet.password = data.get("password", planet.password)
    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    people_id = request.json.get("people_id")
    fav = FavoritePeople.query.filter_by(people_id = people_id).first()
    if not fav:
        return ("Not found", 404)
    db.session.delete(fav)
    db.session.commit()
    return ("Deleted", 204)



