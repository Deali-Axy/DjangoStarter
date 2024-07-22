from typing import Optional, Any

from django.http import HttpRequest
from ninja.security import HttpBearer

from .services import decode


class JwtBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        payload = decode(token)
        if payload:
            return True
        return False
