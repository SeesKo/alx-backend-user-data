#!/usr/bin/env python3
"""
Module for session authentication views
"""
from flask import Blueprint, jsonify, request, make_response
from models.user import User
import os


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """
    Handles user login and session creation
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Import auth dynamically to avoid circular imports
    from api.v1.app import auth

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)

    response = make_response(jsonify(user.to_json()))
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Logs out the current authenticated user
    by destroying their session
    """
    # Import auth dynamically to avoid circular imports
    from api.v1.app import auth

    if not auth.destroy_session(request):
        return jsonify({"error": "Not found"}), 404

    return jsonify({}), 200


@app_views.route('/users/me', methods=['GET'], strict_slashes=False)
def me():
    """
    Retrieve the current authenticated user's information
    """
    # Import auth dynamically to avoid circular imports
    from api.v1.app import auth

    current_user = auth.current_user(request)
    if not current_user:
        return jsonify({"error": "Not found"}), 404

    return jsonify(current_user.to_json())
