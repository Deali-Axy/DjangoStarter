from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    """Landing Page"""
    if request.user.is_authenticated:
        return dashboard(request)
    return render(request, 'home/index.html', {
        'title': 'DjangoStarter',
    })

@login_required
def dashboard(request):
    """Dashboard Page"""
    return render(request, 'home/dashboard.html', {
        'title': 'Dashboard',
        'breadcrumbs': [
            {'text': 'Home', 'url': None, 'icon': 'fa-solid fa-home'},
        ]
    })
