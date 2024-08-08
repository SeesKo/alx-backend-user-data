#!/usr/bin/env python3
"""
Module for session DB authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session DB Authentication """

    def create_session(self, user_id=None):
        """ Creates a session and stores it in the database """
        session_id = super().create_session(user_id)
        if session_id:
            UserSession.create(user_id, session_id)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns user ID from session ID stored in the database """
        if session_id is None:
            return None
        user_session = UserSession.get(session_id)
        if user_session:
            return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """ Destroys a session based on the request cookie """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        UserSession.delete(session_id)
        return True
