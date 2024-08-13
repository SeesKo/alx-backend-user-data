#!/usr/bin/env python3
"""
Flask app with user registration
"""
from flask import Flask, abort, jsonify, request, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home() -> str:
    """
    GET route to return a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """
    POST users route to register a new user.
    """
    email: str = request.form.get("email")
    password: str = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Log in a user and create a session."""
    email: Optional[str] = request.form.get("email")
    password: Optional[str] = request.form.get("password")

    if not email or not password:
        abort(400, description="Missing email or password")

    if AUTH.valid_login(email, password):
        session_id: str = AUTH.create_session(email)
        response: Response = make_response(
            jsonify({"email": email, "message": "logged in"})
        )
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401, description="Invalid credentials")
