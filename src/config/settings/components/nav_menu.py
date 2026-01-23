from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

NAV_MENU = [
    {
        "heading": None,
        "items": [
            {
                "name": _('Home'),
                "url": reverse_lazy('home:index'),
                "icon": 'fa-solid fa-home',
                "match_app": 'home'
            },
            {
                "name": _('About'),
                "url": reverse_lazy('djs_about:index'),
                "icon": 'fa-solid fa-circle-info',
                "match_app": 'djs_about'
            }
        ]
    },
    {
        "heading": _('Applications'),
        "items": [
            {
                "name": _('Demo'),
                "url": reverse_lazy('demo:index'),
                "icon": 'fa-solid fa-layer-group',
                "match_app": 'demo'
            }
        ]
    },
    {
        "heading": _('Account'),
        "items": [
            {
                "name": _('Profile'),
                "url": reverse_lazy('account:index'),
                "icon": 'fa-solid fa-user',
                "match_app": 'account',
                "permissions": ['is_authenticated']
            },
            {
                "name": _('Settings'),
                "url": reverse_lazy('account:settings'),
                "icon": 'fa-solid fa-cog',
                "match_app": 'account',
                "permissions": ['is_authenticated']
            },
            {
                "name": _('Notifications'),
                "url": reverse_lazy('djs_notifications:index'),
                "icon": 'fa-regular fa-bell',
                "match_app": 'djs_notifications',
                "permissions": ['is_authenticated']
            },
            {
                "name": _('Tasks'),
                "url": reverse_lazy('djs_notifications:tasks'),
                "icon": 'fa-solid fa-list-check',
                "match_app": 'djs_notifications',
                "permissions": ['is_authenticated']
            },
            {
                "name": _('Login'),
                "url": reverse_lazy('account:login'),
                "icon": 'fa-solid fa-sign-in-alt',
                "permissions": ['!is_authenticated']
            }
        ]
    }
]
