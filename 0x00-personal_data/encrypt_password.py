#!/usr/bin/env python3
"""
Password encryption module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt with a salt.
    """
    # Encode the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a hashed password
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    """
    # Encode the password to bytes
    password_bytes = password.encode('utf-8')
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password_bytes, hashed_password)
