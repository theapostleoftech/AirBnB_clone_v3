#!/usr/bin/python3
"""This holds views for places amenities"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place

from os import getenv

current_storage = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET'])
def amenity_places_route(place_id):
    """This endpoint lists all the amenities in a place"""
    place_by_id = storage.get(Place, place_id)
    if place_by_id is not None:
        return jsonify([amenity.to_dict() for amenity in place_by_id.amenities])
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity_place_id_route(place_id, amenity_id):
    """This endpoint deletes an amenity"""
    place_by_id = storage.get(Place, place_id)
    if place_by_id:
        amenity_by_id = storage.get(Amenity, amenity_id)
        if amenity_by_id:
            if current_storage != "db":
                if amenity_by_id.id not in place_by_id.amenity_ids:
                    abort(404)
                place_by_id.amenity_ids.remove(amenity_by_id.id)
            else:
                if amenity_by_id not in place_by_id.amenities:
                    abort(404)
                place_by_id.amenities.remove(amenity_by_id)
            storage.save()
            return jsonify({}), 200
        abort(404)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['POST'])
def post_amenity_place_route(place_id, amenity_id):
    """This endpoint creates an amenity"""
    place_by_id = storage.get(Place, place_id)
    amenity_by_id = storage.get(Amenity, amenity_id)
    if place_by_id is None or amenity_by_id is None:
        abort(404)
    if current_storage != "db":
        if amenity_by_id.id in place_by_id.amenity_ids:
            return jsonify(amenity_by_id.to_dict()), 200
        place_by_id.amenity_ids.append(amenity_by_id.id)
        storage.save()
        return jsonify(amenity_by_id.to_dict()), 201
    if amenity_by_id in place_by_id.amenities:
        return jsonify(amenity_by_id.to_dict()), 200
    place_by_id.amenities.append(amenity_by_id)
    storage.save()
    return jsonify(amenity_by_id.to_dict()), 201
