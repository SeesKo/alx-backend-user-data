#!/usr/bin/env python3
"""
Flask app with user registration
"""
from flask import Flask, abort, jsonify, redirect, request, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home() -> str:
    """GET route to return a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """POST users route to register a new user.
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
    """Log in a user and create a session
    """
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Log out a user by destroying the session
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    # Destroy the session for the user
    AUTH.destroy_session(user.id)

    # Redirect to the homepage
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """Handle GET /profile request
    """
    # Get session_id from cookies
    session_id = request.cookies.get('session_id')

    # Find the user based on session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Handle the POST /reset_password route
    """
    email = request.form.get('email')

    if not email:
        abort(400)
    try:
        # Generate reset password token
        reset_token = AUTH.get_reset_password_token(email)
        # Return JSON response
        return jsonify({
            'email': email,
            'reset_token': reset_token
        }), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Handles the password update
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400)  # Bad Request if any field is missing

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
