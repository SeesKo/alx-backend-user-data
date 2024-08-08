#!/usr/bin/env python3
"""
Module for Session Authentication
"""
from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Session Authentication class that inherits from Auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session ID for a given user_id.
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        # Generate a new session ID
        session_id = str(uuid.uuid4())

        # Store the session ID in the dictionary with the user_id
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve a user ID for a given session ID.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        # Retrieve the user ID from the dictionary using the session ID
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieve the current user based on the session cookie.
        """
        if request is None:
            return None

        # Retrieve the session ID from the cookie
        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        # Retrieve the User instance from the database
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Destroys the user session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
