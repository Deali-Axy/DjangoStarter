from django.shortcuts import render, redirect
from django.contrib import messages
from .models import About, Contact
from .forms import ContactForm

def index(request):
    # 获取最新的About数据
    about = About.objects.first()
    
    # 如果数据库中没有数据，使用默认值
    if not about:
        about = {
            'story': '我们是一个充满激情的团队，致力于为用户提供最优质的服务。我们相信通过不断创新和改进，可以为用户带来更好的体验。',
            'mission': '通过技术创新推动行业发展，为用户创造价值，让科技更好地服务于人。',
            'email': 'contact@example.com',
            'phone': '400-123-4567',
            'address': '中国北京市朝阳区科技园区888号'
        }
    
    return render(request, 'django_starter/about/index.html', {'about': about})

def contact(request):
    about = About.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                message=form.cleaned_data['message']
            )
            messages.success(request, '感谢您的留言，我们会尽快与您联系！')
            return redirect('about/contact')
    else:
        form = ContactForm()

    return render(request, 'django_starter/about/contact.html', {
        'form': form,
        'about': about
    })

def privacy_policy(request):
    return render(request, 'django_starter/about/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'django_starter/about/terms_of_service.html')
