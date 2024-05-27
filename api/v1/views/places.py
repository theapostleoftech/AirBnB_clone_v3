#!/usr/bin/python3
"""This handles the views for the place objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def retrieve_places_in_city_route(city_id):
    """THis endpoint lists all places object in a city"""
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def retrieve_place_route(place_id):
    """This endpoint retrieves a place object"""
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_place_route(place_id):
    """This endpoint deletes a place object"""
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def create_place_route(city_id):
    """Create a new place in a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_data = request.get_json()
    if not place_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in place_data:
        abort(400, 'Missing user_id')
    user_id = request.get_json()["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_place = Place(**place_data())
    new_place.city_id = city_id
    new_place.user_id = user.id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['PUT'])
def update_place_route(place_id):
    """This endpoint updates a place object"""
    place_data = request.get_json()
    if not place_data:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place is not None:
        for attr, value in place_data().items():
            if (hasattr(place, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_at' and attr != 'user_id' and
                    attr != 'city_id'):
                setattr(place, attr, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    abort(404)
