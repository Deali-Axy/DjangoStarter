from django.utils.csp import CSP

# 宽松模式
# 引入任何 HTTPS 的 CDN 资源（JS/CSS/图片/字体）都不会报错，
# 直接写在 HTML 里的 <script> 和 <style> 也能正常执行。
SECURE_CSP = {
    # Default : 只允许同源 ( self )
    "default-src": [CSP.SELF],
    # Script : 允许同源、内联脚本 ( unsafe-inline )、 eval ( unsafe-eval ) 以及任何 HTTPS 来源 ( https: )。
    "script-src": [CSP.SELF, CSP.UNSAFE_EVAL, CSP.UNSAFE_INLINE, "https:"],
    # Style : 允许同源、内联样式 ( unsafe-inline ) 以及任何 HTTPS 来源 ( https: )。
    "style-src": [CSP.SELF, CSP.UNSAFE_INLINE, "https:"],
    # Img/Font/Connect : 允许同源和任何 HTTPS 来源。
    "img-src": [CSP.SELF, "https:", "data:"],
    "font-src": [CSP.SELF, "https:", "data:"],
    "connect-src": [CSP.SELF, "https:"],
    "frame-ancestors": [CSP.SELF],
}
