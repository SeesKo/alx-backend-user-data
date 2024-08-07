#!/usr/bin/env python3
"""
This module sets up the Flask application and handles API routing,
authentication, and error handling.
"""
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """Handle requests before they reach the view function.

    This method checks if the request path requires authentication,
    and if so, verifies the authorization header or session cookie.
    Aborts with 401 or 403 if authentication fails.
    """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'  # Excluded path for authentication
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    # Check authorization header and session cookie
    if (auth.authorization_header(request) is None and
            auth.session_cookie(request) is None):
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """Return a JSON response for 404 errors.

    Args:
        error: The error object.

    Returns:
        A JSON response with an error message and status code 404.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Return a JSON response for 401 errors.

    Args:
        error: The error object.

    Returns:
        A JSON response with an error message and status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Return a JSON response for 403 errors.

    Args:
        error: The error object.

    Returns:
        A JSON response with an error message and status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
