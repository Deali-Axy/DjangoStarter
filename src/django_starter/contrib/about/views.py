from django.shortcuts import render
from django_starter.contrib.about.models import About

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
    
    # 准备传递给模板的上下文数据
    context = {
        'about': about
    }
    
    return render(request, 'django_starter/about/index.html', context)
