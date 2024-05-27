#!/usr/bin/python3
"""This holds the views to the amenities API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False,
                 methods=['GET'])
def retrieve_amenities_route():
    """This endpoint lists all amenities objects"""
    return jsonify([amenity.to_dict() for
                    amenity in storage.all(Amenity).values()])


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def retrieve_amenity_route(amenity_id):
    """This endpoint retrieves an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity_route(amenity_id):
    """This endpoint deletes an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", strict_slashes=False,
                 methods=['POST'])
def create_amenity_route():
    """This endpoint creates an amenity object"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, 'Not a JSON')
    if 'name' not in amenity_data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**amenity_data())
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def update_amenity_route(amenity_id):
    """This endpoint updates an amenity object"""
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        for attr, value in request.get_json().items():
            if (hasattr(amenity, attr) and
                    attr != 'id' and attr != 'created_at' and
                    attr != 'updated_at'):
                setattr(amenity, attr, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
