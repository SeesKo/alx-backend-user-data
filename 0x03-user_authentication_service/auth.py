#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
from uuid import uuid4
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the salted hash
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a new UUID and returns it as a string
    """
    return str(uuid4())


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
            # Check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, proceed to create a new user
            user = self._db.add_user(email, _hash_password(password))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials for a user
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except (NoResultFound, AttributeError):
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for the user with the given email."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
        self, session_id: Optional[str]
    ) -> Optional[User]:
        """Get a user based on session_id.
        """
        if session_id is None:
            return None
        try:
            # Find the user by session_id using public method `find_user_by`
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session by updating user's session_id to None.
        """
        if user_id is None:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for user then returns it
        """
        try:
            # Try to find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        except InvalidRequestError:
            raise ValueError

        # Generate a new UUID token
        reset_token = str(uuid4())
        # Update the user's reset token in the database
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates user's password using the provided reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            # If no user found with given reset_token, raise ValueError
            raise ValueError

        # Hash the new password
        hashed_password = _hash_password(password)

        # Update the user's password and reset token in the database
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None
        )
