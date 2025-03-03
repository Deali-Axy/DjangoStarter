from django.shortcuts import render


# Create your views here.
def index(request):
    print(request.LANGUAGE_CODE)
    return render(request, 'demo/index.html')
