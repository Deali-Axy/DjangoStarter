from django.shortcuts import render
from . import config

class Uri(object):
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url


def index(request):
    ctx = {
        'projects': config.PROJECTS,
        'blogs': config.BLOGS
    }
    return render(request, 'django_starter/guide/index.html', ctx)
