from typing import Dict, List, Union

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

REFERRER_POLICY = 'same-origin'

PERMISSIONS_POLICY: Dict[str, Union[str, List[str]]] = {}  # noqa: WPS234
