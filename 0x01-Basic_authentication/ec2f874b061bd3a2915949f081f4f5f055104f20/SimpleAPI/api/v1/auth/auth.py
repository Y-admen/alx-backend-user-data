from typing import List, TypeVar


class Auth:
    def authorization_header(self, request=None) -> str:
        """return the value of the header request Authorization"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            if path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
