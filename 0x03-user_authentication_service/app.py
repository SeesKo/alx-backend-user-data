#!/usr/bin/env python3
"""
Flask app with user registration
"""
from flask import Flask, jsonify, request, Response, abort
from auth import Auth
from typing import Dict, Union


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome() -> Response:
    """
    GET route to return a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> Union[Response, tuple]:
    """
    POST users route to register a new user.
    """
    email: str = request.form.get("email")
    password: str = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
