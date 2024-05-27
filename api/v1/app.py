#!/usr/bin/python3
"""Handles the views blueprint"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def _storage(self):
    """This closes the database connection"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """This endpoint returns a 404 error"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
