#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import jsonify
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
auth_type = getenv('AUTH_TYPE')
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request():
    """
    This function is executed before any request is processed by the Flask app.

    It checks if the `auth` object is set, and if so,
    it performs the following:
    This function is used to ensure that all requests to the API are
    authenticated and authorized, except for the `/api/v1/status/`,
    `/api/v1/unauthorized/`, and `/api/v1/forbidden/` endpoints, which are
    excluded from authentication and authorization checks.
    """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """
    Returns a JSON response with an
    "Unauthorized" error message and a 401 code.

    Parameters:
    - error: The error message.

    Returns:
    - A JSON response with the error message and a status code of 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Returns a JSON response with a 403 Forbidden error.

    Parameters:
    - error (str): The error message.

    Returns:
    - response (json): A JSON response with the error message and status 403.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
