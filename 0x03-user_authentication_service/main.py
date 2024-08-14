#!/usr/bin/env python3
"""
Integration tests for user authentication.
"""
import requests


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


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    profile_unlogged()
