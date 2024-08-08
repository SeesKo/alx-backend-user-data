#!/usr/bin/env python3
"""
Module for Session Authentication views
"""
from flask import Blueprint, request, jsonify, make_response
from models.user import User
from api.v1.app import auth
from os import getenv


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


@app_views.route(
    '/auth_session/login/', methods=['POST'],
    strict_slashes=False
)
def login() -> str:
    """
    Handle user login and create session.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search(email)
    if user is None:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the user
    session_id = auth.create_session(user.id)
    if session_id is None:
        return jsonify({"error": "failed to create session"}), 500

    # Prepare the response with the User JSON representation
    response = jsonify(user.to_json())

    # Set the session cookie
    session_name = getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(session_name, session_id)

    return response
