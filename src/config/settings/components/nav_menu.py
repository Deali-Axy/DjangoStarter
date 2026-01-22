from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

NAV_MENU = [
    {
        'name': _('Home'),
        'url': reverse_lazy('home:index'),
        'icon': 'fa-solid fa-house-laptop'
    },
    {
        'name': _('About'),
        'url': reverse_lazy('djs_about:index'),
        'icon': 'fa-solid fa-circle-info'
    }
]
