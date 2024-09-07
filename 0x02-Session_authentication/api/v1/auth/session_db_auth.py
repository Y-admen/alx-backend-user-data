#!/usr/bin/env python3
"""Handling API Authentication

Authentication method: session cookie with expiration
"""

from datetime import datetime, timedelta
from uuid import uuid4

from models.user_session import UserSession

from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session Auth with Expiration"""

    def create_session(self, user_id: str = None) -> str:
        """Create a new login session"""
        if not user_id:
            return
        session = UserSession(user_id=user_id, session_id=str(uuid4()))
        session.save()
        return session.session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get user id based on session_id"""
        session = UserSession.search({"session_id": session_id})
        if len(session) == 0:
            return
        session = session[0]
        user_id = session.user_id
        if self.session_duration <= 0:
            return user_id
        if session.created_at:
            diff: timedelta = datetime.utcnow() - session.created_at
            if diff.total_seconds() > self.session_duration:
                session.remove()
            else:
                return session.user_id

    def destroy_session(self, request=None):
        """Delete the current session and logout"""
        session_id = self.session_cookie(request)
        if session_id:
            session = UserSession.search({"session_id": session_id})
            if len(session) > 0:
                session[0].remove()
                return True
        return False
