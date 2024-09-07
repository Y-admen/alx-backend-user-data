#!/usr/bin/env python3
"""Handling API Authentication based on the Basic scheme"""

import base64
from typing import TypeVar


from .auth import Auth


class BasicAuth(Auth):
    """Authentication handler for the Basic scheme"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # nopep8
        """Get the base64 encoded string from the authorization header"""
        if isinstance(authorization_header, str):
            if authorization_header.startswith("Basic "):
                return authorization_header.rstrip()[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # nopep8
        """Decode a base64 encoded string"""
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # nopep8
        """Get the username, password from a decoded authorization header"""
        if isinstance(decoded_base64_authorization_header, str):
            if ":" in decoded_base64_authorization_header:
                return tuple(decoded_base64_authorization_header.split(":", 1))
        return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # nopep8
        """Get the user object based on his email and password"""
        from models.user import User
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            users = User.search({"email": user_email})
            if len(users) > 0 and users[0].is_valid_password(user_pwd):
                return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current logged in user, Basic Authentication shceme"""
        ah = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(ah)
        b64_decoded = self.decode_base64_authorization_header(b64)
        email, pwd = self.extract_user_credentials(b64_decoded)
        return self.user_object_from_credentials(email, pwd)
