#!/usr/bin/python3
"""This handles views for cities"""

from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieve_cities_route(state_id):
    """This endpoint lists all city objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def retrieve_city_route(city_id):
    """This endpoint retrives a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city_route(city_id):
    """This endpoint deletes a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city_route(state_id):
    """This endpoint creates a city object belonging to a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_data = request.get_json()
    if city_data is None:
        abort(400, 'Not a JSON')

    if 'name' not in city_data:
        abort(400, 'Missing name')
    city_data['state_id'] = state_id
    city = City(**city_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_state_route(city_id):
    """This endpoint updates a state object"""
    city_data = request.get_json
    if city_data is None:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, value in city_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']
        setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
