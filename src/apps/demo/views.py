from django.shortcuts import render
from django.core.exceptions import PermissionDenied


# Create your views here.
def index(request):
    print(request.LANGUAGE_CODE)
    return render(request, 'demo/index.html')


def test_403(request):
    raise PermissionDenied()


def test_404(request):
    # Django会自动处理不存在的URL，返回404页面
    # 这里我们手动返回404模板
    return render(request, '404.html', status=404)


def test_500(request):
    # 故意制造一个异常来触发500错误
    raise Exception("这是一个测试用的500错误！")
