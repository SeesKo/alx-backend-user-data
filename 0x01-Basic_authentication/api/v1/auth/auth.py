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
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Returns the current user based on the request
        """
        return None
