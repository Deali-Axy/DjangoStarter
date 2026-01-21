from typing import Dict, List, Union

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Django 4.0+ 增强了 CSRF 保护机制，会对 Origin 和 Host 进行严格比对
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://localhost',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

X_FRAME_OPTIONS = 'DENY'

REFERRER_POLICY = 'same-origin'

PERMISSIONS_POLICY: Dict[str, Union[str, List[str]]] = {}  # noqa: WPS234
