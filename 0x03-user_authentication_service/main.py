#!/usr/bin/env python3
"""
Integration tests for user authentication.
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Registers a new user and asserts the response
    """
    response = requests.post(
        f"{BASE_URL}/users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def profile_unlogged() -> None:
    """Accesses profile without logging in and asserts the response
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    # log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    # session_id = log_in(EMAIL, PASSWD)
    # profile_logged(session_id)
    # log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
