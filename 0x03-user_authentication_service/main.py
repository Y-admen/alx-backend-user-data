#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

session_id = auth.create_session(email)
print(session_id)  # Expected output: a new UUID

user = auth.get_user_from_session_id(session_id)
print(user.email)  # Expected output: bob@bob.com

invalid_session_id = "invalid_session_id"
user = auth.get_user_from_session_id(invalid_session_id)
print(user)  # Expected output: None
