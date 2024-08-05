#!/usr/bin/env python3
"""
Authentication module for the API
"""
from typing import List, TypeVar
from flask import request


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
            # Check if the path matches the excluded_path
            if path == excluded_path or path.startswith(excluded_path):
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
        return None
