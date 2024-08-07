#!/usr/bin/env python3
"""
Authentication module for the API
"""
from typing import List, TypeVar
from flask import request
import fnmatch
import os


User = TypeVar('User')


class Auth:
    """Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a path requires authentication
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path ends with a '/'
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            # Ensure excluded_path ends with a '/'
            excluded_path = excluded_path.rstrip('/') + '/'
            # Use fnmatch to check for wildcard matches
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """
        Returns the current user based on the request
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def session_cookie(self, request=None) -> str:
        """
        Returns the session cookie value from the request
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
