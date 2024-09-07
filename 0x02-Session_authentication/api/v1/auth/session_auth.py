#!/usr/bin/env python3
"""Handling API Authentication

Authentication method: session cookie
"""

from uuid import uuid4

from models.user import User

from .auth import Auth


class SessionAuth(Auth):
    """Authentication handler for the Basic scheme"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session id"""
        if isinstance(user_id, str):
            s_id = str(uuid4())
            self.user_id_by_session_id[s_id] = user_id
            return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get the user's id based on session id"""
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Get the current user based on session authentication"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Delete a user session & logout"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            del self.user_id_by_session_id[session_id]
            return True
        return False
