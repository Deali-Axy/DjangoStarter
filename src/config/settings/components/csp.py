from django.utils.csp import CSP

SECURE_CSP = {
    "default-src": [CSP.SELF],
    "script-src": [CSP.SELF, CSP.NONCE],
    "style-src": [CSP.SELF, CSP.NONCE],
    "img-src": [CSP.SELF, "https:", "data:"],
    "font-src": [CSP.SELF, "https:", "data:"],
    "connect-src": [CSP.SELF],
    "frame-ancestors": [CSP.SELF],
}
