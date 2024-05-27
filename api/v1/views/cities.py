#!/usr/bin/python3
"""This holds the endpoints for cities"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def retrieve_cities_route(state_id):
    """This endpoint lists all city objects of a state"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def retrieve_city_route(city_id):
    """This endpoint retrieves a city object"""
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_city_route(city_id):
    """This endpoint deletes a city object"""
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def create_city_route(state_id):
    """This endpoint creates a city object belonging to a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        abort(400, 'Not a JSON')
    if 'name' not in city_data:
        abort(400, 'Missing name')
    new_city = City(**city_data())
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("cities/<city_id>", strict_slashes=False, methods=['PUT'])
def update_city_route(city_id):
    """This endpoint updates a city object"""
    city_data = request.get_json()
    if not city_data:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city is not None:
        for attr, value in city_data().items():
            setattr(city, attr, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    abort(404)
