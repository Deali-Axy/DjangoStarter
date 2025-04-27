from django.utils.translation import gettext_lazy as _

from config.settings.components.django_starter import DJANGO_STARTER

UNFOLD = {
    "SITE_TITLE": DJANGO_STARTER['admin']['site_title'],
    "SITE_HEADER":  DJANGO_STARTER['admin']['site_header'],
    "SITE_SUBHEADER": '',
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("项目主页"),
            "link": "https://github.com/Deali-Axy/DjangoStarter",
        },
    ],
}