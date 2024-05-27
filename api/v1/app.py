#!/usr/bin/python3
"""Handles the views blueprint"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_route(error):
    """This endpoint return a 404 error"""
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown_storage(exception):
    """This closes database connections"""
    storage.close()


if '__name__' == '__main__':
    app.run('0.0.0.0', port='5000', threaded=True)
