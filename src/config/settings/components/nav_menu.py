from django.urls import reverse_lazy

NAV_MENU = [
    {
        'name': '主页',
        'url': reverse_lazy('djs_guide:index'),
        'icon': 'fa-solid fa-house-laptop'
    },
    {
        'name': '关于',
        'url': reverse_lazy('djs_about:index'),
        'icon': 'fa-solid fa-circle-info'
    }
]
