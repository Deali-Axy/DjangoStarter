from django.http import JsonResponse
from django.shortcuts import render
from django.tasks import task
from . import config

class Uri(object):
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url


def index(request):
    record_guide_visit.enqueue(path=request.path)
    ctx = {
        'projects': config.PROJECTS,
        'blogs': config.BLOGS
    }
    return render(request, 'django_starter/guide/index.html', ctx)


@task
def record_guide_visit(path: str) -> str:
    return path


def enqueue_task(request):
    record_guide_visit.enqueue(path=request.path)
    return JsonResponse({'queued': True})
