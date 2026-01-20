from django.utils.csp import CSP

SECURE_CSP = {
    # To enforce a CSP policy:
    "default-src": [CSP.SELF],
    # Allow self-hosted scripts and script tags with matching `nonce` attr.
    "script-src": [CSP.SELF, CSP.NONCE],
    "style-src": [CSP.SELF, CSP.NONCE],
    "img-src": [CSP.SELF, "https:", "data:"],
    "font-src": [CSP.SELF, "https:", "data:"],
    "connect-src": [CSP.SELF],
    "frame-ancestors": [CSP.SELF],
}
