#!/usr/bin/env python3
"""
Module for session expiration authentication
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Class to manage session expiration """

    def __init__(self):
        """ Initialize SessionExpAuth """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a session ID with expiration """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return user ID from session ID, considering expiration """
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        if self.session_duration <= 0:
            return session_data.get("user_id")

        created_at = session_data.get("created_at")
        if created_at is None:
            return None

        if datetime.now() > (
            created_at + timedelta(seconds=self.session_duration)
        ):
            return None

        return session_data.get("user_id")
