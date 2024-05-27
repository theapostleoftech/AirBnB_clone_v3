#!/usr/bin/python3
"""This contains all API endpoints"""
from api.v1.views import app_views
from models import storage

from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status_route():
    """This endpoint returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', strict_slashes=False)
def stats_route():
    """This endpoint retrieves the number of each objects by type"""
    objects = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(objects)