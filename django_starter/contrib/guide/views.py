from django.shortcuts import render


class Uri(object):
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url


def index(request):
    blogs = [
        Uri('项目完成小结 - Django-React-Docker-Swag部署配置', 'https://www.cnblogs.com/deali/p/16961771.html'),
        Uri('Django更换数据库和迁移数据方案', 'https://www.cnblogs.com/deali/p/16884908.html'),
        Uri('DjangoAdmin使用合集，它的功能比你想象的强大！', 'https://www.cnblogs.com/deali/p/16678014.html'),
        Uri('轻量级消息队列 Django-Q 轻度体验', 'https://www.cnblogs.com/deali/p/16644989.html'),
        Uri('Django-Import-Export插件控制数据导入流程', 'https://www.cnblogs.com/deali/p/16636562.html'),
        Uri('Django数据库性能优化之 - 使用Python集合操作', 'https://www.cnblogs.com/deali/p/16449011.html'),
    ]
    projects = [
        Uri('excel_to_model', 'https://github.com/Deali-Axy/excel_to_model'),
        Uri('django / channels', 'https://github.com/django/channels'),
        Uri('Koed00 / django-q', 'https://github.com/Koed00/django-q'),
        Uri('axnsan12 / drf-yasg', 'https://github.com/axnsan12/drf-yasg'),
    ]
    ctx = {
        'projects': projects,
        'blogs': blogs
    }
    return render(request, 'django_starter/guide/index.html', ctx)
