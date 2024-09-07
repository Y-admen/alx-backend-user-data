#!/usr/bin/env python3
"""Handling API Authentication

Authentication method: session cookie with expiration
"""

from datetime import datetime, timedelta
from os import getenv
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Auth with Expiration"""

    def __init__(self) -> None:
        """Initialize a new authentication object"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Create a new session for user_id"""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "created_at": datetime.now(),
                "user_id": user_id,
            }
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get the user_id based on session_id"""
        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return
        user = session.get("user_id")
        if self.session_duration <= 0:
            return user
        created_at = session.get("created_at")
        if created_at:
            diff: timedelta = datetime.now() - created_at
            if diff.total_seconds() > self.session_duration:
                del self.user_id_by_session_id[session_id]
            else:
                return user
