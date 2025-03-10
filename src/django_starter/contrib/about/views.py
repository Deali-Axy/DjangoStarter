from types import SimpleNamespace
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from .models import About, Contact
from .forms import ContactModelForm


def get_about():
    # 获取最新的About数据
    about = About.objects.first()

    # 如果数据库中没有数据，使用默认值
    if not about:
        about = {
            'story': '我们是一个充满激情的团队，致力于为用户提供最优质的服务。我们相信通过不断创新和改进，可以为用户带来更好的体验。',
            'mission': '通过技术创新推动行业发展，为用户创造价值，让科技更好地服务于人。',
            'values': [
                {'title': '创新', 'icon': 'fa-brands fa-bluesky',
                 'description': '持续创新是我们的核心驱动力，我们始终保持开放和进取的心态。'},
                {'title': '品质', 'icon': 'fa-solid fa-shield-halved',
                 'description': '追求卓越品质，为客户提供最优质的产品和服务。'},
                {'title': '协作', 'icon': 'fa-solid fa-handshake-simple',
                 'description': '团队协作是我们的基石，共同创造更大的价值。'}
            ],
            'milestones': [
                {'year': '2020', 'title': '公司成立', 'description': '公司成立，开始专注于技术创新和产品研发'},
                {'year': '2021', 'title': '产品发布', 'description': '成功推出首个产品，获得市场认可'},
                {'year': '2022', 'title': '团队扩张', 'description': '团队规模扩大到100人，业务范围覆盖全国'},
                {'year': '2023', 'title': 'A轮融资', 'description': '获得A轮融资，加速产品迭代和市场扩张'}
            ],
            'metrics': [
                {'label': '服务用户', 'value': '150000'},
                {'label': '项目案例', 'value': '3000'},
                {'label': '合作伙伴', 'value': '80'},
                {'label': '客户满意度', 'value': '100'}
            ],
            'email': 'contact@example.com',
            'phone': '400-123-4567',
            'address': '中国北京市朝阳区科技园区888号'
        }
        about = SimpleNamespace(**about)

    return about


def index(request):
    about = get_about()
    return render(request, 'django_starter/about/index.html', {'about': about})


def contact(request):
    about = get_about()
    contact_info = [
        {'icon': 'fas fa-envelope', 'name': '邮箱', 'value': about.email},
        {'icon': 'fas fa-phone', 'name': '电话', 'value': about.phone},
        {'icon': 'fas fa-location-dot', 'name': '地址', 'value': about.address},
        {'icon': 'fa-solid fa-earth-americas', 'name': '网站', 'value': 'https://github.com/Deali-Axy/django-starter'},
        {'icon': 'fa-brands fa-x-twitter', 'name': 'Twitter', 'value': 'DjangoStarter'},
        {'icon': 'fa-brands fa-facebook-f', 'name': 'Facebook', 'value': 'DjangoStarter'},
        {'icon': 'fa-brands fa-weixin', 'name': '微信', 'value': 'DjangoStarter'},
        {'icon': 'fa-brands fa-weibo', 'name': '微博', 'value': 'DjangoStarter'},
    ]
    template_name = 'django_starter/about/contact.html'
    context = {
        'form': ContactModelForm(),
        'contact_info': contact_info,
    }

    if request.method == 'POST':
        if not settings.DJANGO_STARTER['site']['enable_contact_form']:
            messages.error(request, '留言功能未启用！')
            return redirect(reverse('djs_about:contact'))

        form = ContactModelForm(request.POST)
        context['form'] = form
        if not form.is_valid():
            messages.error(request, '信息校验失败，请检查无误再提交')
            return render(request, template_name, context)

        form.save()
        messages.success(request, '感谢您的留言，我们会尽快与您联系！')
        return redirect(reverse('djs_about:contact'))

    return render(request, template_name, context)


def privacy_policy(request):
    return render(request, 'django_starter/about/privacy_policy.html')


def terms_of_service(request):
    return render(request, 'django_starter/about/terms_of_service.html')
