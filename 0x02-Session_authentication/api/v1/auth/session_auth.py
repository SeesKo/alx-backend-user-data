#!/usr/bin/env python3
"""
Module for Session Authentication
"""
from .auth import Auth
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
