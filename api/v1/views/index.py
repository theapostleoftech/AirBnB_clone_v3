#!/usr/bin/python3
"""This contains routes for app_views"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_route():
    """This endpoint lists the status of the api"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats_route():
    """This endpoint retrieves the number of each objects by type"""
    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count('City'),
                    "places": storage.count('Place'),
                    "reviews": storage.count('Review'),
                    "states": storage.count('State'),
                    "users": storage.count('User')})
