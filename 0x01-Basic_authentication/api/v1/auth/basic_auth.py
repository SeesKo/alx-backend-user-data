#!/usr/bin/env python3
"""
Basic Authentication module for the API
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ Basic Authentication class that inherits from Auth """

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        Extract the Base64 part of the Authorization
        header for Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        Decode the Base64 part of the Authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(base64_bytes)
            return decoded_bytes.decode('utf-8')
        except (TypeError, base64.binascii.Error):
            return None
