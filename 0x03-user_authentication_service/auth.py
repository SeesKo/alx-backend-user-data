#!/usr/bin/env python3
"""
Authentication module
"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import bcrypt


def _hash_password(self, password: str) -> bytes:
    """Hashes a password using bcrypt
    and returns the salted hash.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialize the Auth class with a database instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with an email and password.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login with email and password."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password.encode('utf-8')
            )
        except NoResultFound:
            return False
