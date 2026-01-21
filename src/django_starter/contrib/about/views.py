from types import SimpleNamespace

from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from django.conf import settings

from .models import About, Contact
from .forms import ContactModelForm


MILESTONES_PAGE_SIZE = 4
TEAM_PAGE_SIZE = 8
FAQ_PAGE_SIZE = 5


def _normalize_metrics(metrics):
    """将 metrics 规范化为 [{label, value, icon}, ...] 结构。"""
    if metrics is None:
        return []

    if isinstance(metrics, list):
        normalized = []
        for item in metrics:
            if not isinstance(item, dict):
                continue
            label = item.get('label')
            value = item.get('value')
            icon = item.get('icon')
            if label is None or value is None:
                continue
            normalized.append({'label': label, 'value': value, 'icon': icon or 'fa-solid fa-arrow-trend-up'})
        return normalized

    if isinstance(metrics, dict):
        icons = {
            '服务用户': 'fa-solid fa-users',
            '项目案例': 'fa-solid fa-diagram-project',
            '合作伙伴': 'fa-solid fa-handshake',
            '客户满意度': 'fa-solid fa-face-smile',
        }
        normalized = []
        for key, value in metrics.items():
            normalized.append({'label': str(key), 'value': value, 'icon': icons.get(str(key), 'fa-solid fa-arrow-trend-up')})
        return normalized

    return []


def _get_default_about():
    """返回默认的 about 页面内容（当数据库未配置时使用）。"""
    payload = {
        'title': 'DjangoStarter',
        'story': '我们是一支以工程质量为核心的团队，专注于把复杂系统做得清晰、稳定且可扩展。',
        'mission': '通过工程化实践与高质量的用户体验，为你更快交付可靠产品。',
        'vision': '让 Django 项目从“能跑”到“可持续演进”，降低长期维护成本。',
        'values': [
            {
                'title': '清晰',
                'icon': 'fa-solid fa-sparkles',
                'description': '信息层级清晰、组件可复用、接口可解释。',
            },
            {
                'title': '可靠',
                'icon': 'fa-solid fa-shield-halved',
                'description': '以可维护性与稳定性为先，减少不可预期的变更成本。',
            },
            {
                'title': '协作',
                'icon': 'fa-solid fa-people-group',
                'description': '用一致的规范与节奏，把跨职能协作变得更高效。',
            },
        ],
        'milestones': [
            {'year': '2020', 'title': '项目启动', 'description': '搭建基础框架与工程化规范'},
            {'year': '2021', 'title': '核心能力沉淀', 'description': '完善认证、权限、脚手架与常用组件'},
            {'year': '2022', 'title': '生产实践验证', 'description': '在真实项目中持续迭代与优化体验'},
            {'year': '2023', 'title': '生态扩展', 'description': '补齐文档、模板与可复用的最佳实践'},
            {'year': '2024', 'title': '体验升级', 'description': '引入更现代的交互与一致的视觉语言'},
            {'year': '2025', 'title': '持续演进', 'description': '围绕可维护性与交付效率继续优化'},
        ],
        'metrics': [
            {'label': '服务用户', 'value': 150000, 'icon': 'fa-solid fa-users'},
            {'label': '项目案例', 'value': 3000, 'icon': 'fa-solid fa-diagram-project'},
            {'label': '合作伙伴', 'value': 80, 'icon': 'fa-solid fa-handshake'},
            {'label': '客户满意度', 'value': 100, 'icon': 'fa-solid fa-face-smile'},
        ],
        'email': 'contact@example.com',
        'phone': '400-123-4567',
        'address': '中国北京市朝阳区科技园区 888 号',
        'team': [
            {'name': 'Lin', 'role': 'Product', 'bio': '负责产品方向与信息架构。', 'links': {'website': 'https://github.com/Deali-Axy/django-starter'}},
            {'name': 'Chen', 'role': 'Design', 'bio': '负责视觉体系与交互一致性。', 'links': {'x': 'https://x.com'}},
            {'name': 'Wang', 'role': 'Frontend', 'bio': '负责模板与交互性能优化。', 'links': {'github': 'https://github.com'}},
            {'name': 'Zhang', 'role': 'Backend', 'bio': '负责安全与可维护性方案。', 'links': {'github': 'https://github.com'}},
            {'name': 'Zhao', 'role': 'QA', 'bio': '负责验收标准与回归策略。', 'links': {'website': 'https://example.com'}},
            {'name': 'Sun', 'role': 'Ops', 'bio': '负责部署与可观测性。', 'links': {'website': 'https://example.com'}},
            {'name': 'He', 'role': 'Data', 'bio': '负责指标体系与分析闭环。', 'links': {'website': 'https://example.com'}},
            {'name': 'Li', 'role': 'Growth', 'bio': '负责增长与内容策略。', 'links': {'website': 'https://example.com'}},
            {'name': 'Zhou', 'role': 'Support', 'bio': '负责客户反馈与支持。', 'links': {'website': 'https://example.com'}},
            {'name': 'Hu', 'role': 'Engineer', 'bio': '负责性能与体验细节。', 'links': {'github': 'https://github.com'}},
        ],
        'faqs': [
            {'q': '为什么选择服务端渲染？', 'a': 'SSR 在可访问性、SEO 与首屏稳定性上更有优势，并能与 HTMX 结合获得更流畅的交互。'},
            {'q': 'Tailwind-only 会限制设计吗？', 'a': '不会。通过统一 token 与组件组合，你可以实现更一致、更可维护的设计系统。'},
            {'q': 'AOS 动效如何避免影响性能？', 'a': '只在关键区块使用轻量动效，统一时长与缓动，并在减少动画偏好下自动禁用。'},
            {'q': '“加载更多”如何实现？', 'a': '使用 HTMX 触发 GET 请求，服务端返回 HTML 片段并更新按钮状态，全程无刷新。'},
            {'q': '如何保证可访问性？', 'a': '坚持语义化结构、合理对比度、键盘可达与清晰的 focus 样式。'},
            {'q': '如何扩展为真实团队数据？', 'a': '可将 team/faqs 迁移为模型字段或通过配置/接口动态提供，模板无需大改。'},
            {'q': '如何保持全站一致风格？', 'a': '复用统一的间距、圆角、阴影与按钮规范，并避免自定义 CSS。'},
        ],
    }
    return SimpleNamespace(**payload)


def get_about():
    """获取 about 页面内容，优先使用数据库配置，不存在则使用默认值。"""
    about = About.objects.first()
    if not about:
        return _get_default_about()

    if not isinstance(about.values, list):
        about.values = []
    if not isinstance(about.milestones, list):
        about.milestones = []
    about.metrics = _normalize_metrics(about.metrics)

    if not getattr(about, 'vision', None):
        about.vision = '成为行业领先的创新者，持续为用户创造价值。'

    if not getattr(about, 'team', None):
        about.team = _get_default_about().team
    if not getattr(about, 'faqs', None):
        about.faqs = _get_default_about().faqs

    return about


def index(request):
    """渲染关于我们主页面。"""
    about = get_about()

    milestones = list(getattr(about, 'milestones', []) or [])
    milestones_initial = milestones[:MILESTONES_PAGE_SIZE]
    milestones_next_offset = len(milestones_initial)

    team = list(getattr(about, 'team', []) or [])
    team_initial = team[:TEAM_PAGE_SIZE]
    team_next_offset = len(team_initial)

    faqs = list(getattr(about, 'faqs', []) or [])
    faqs_initial = faqs[:FAQ_PAGE_SIZE]
    faqs_next_offset = len(faqs_initial)

    context = {
        'about': about,
        'metrics': _normalize_metrics(getattr(about, 'metrics', [])),
        'milestones_initial': milestones_initial,
        'milestones_has_more': milestones_next_offset < len(milestones),
        'milestones_next_offset': milestones_next_offset,
        'team_initial': team_initial,
        'team_has_more': team_next_offset < len(team),
        'team_next_offset': team_next_offset,
        'faqs_initial': faqs_initial,
        'faqs_has_more': faqs_next_offset < len(faqs),
        'faqs_next_offset': faqs_next_offset,
    }
    return render(request, 'django_starter/about/index.html', context)


def partials_milestones(request):
    """HTMX：分页返回更多里程碑条目。"""
    about = get_about()
    milestones = list(getattr(about, 'milestones', []) or [])

    try:
        offset = int(request.GET.get('offset', '0'))
    except ValueError:
        offset = 0
    offset = max(0, offset)

    page = milestones[offset:offset + MILESTONES_PAGE_SIZE]
    next_offset = offset + len(page)

    context = {
        'milestones': page,
        'has_more': next_offset < len(milestones),
        'next_offset': next_offset,
    }
    return render(request, 'django_starter/about/partials/milestones.html', context)


def partials_team(request):
    """HTMX：分页返回更多团队成员卡片。"""
    about = get_about()
    team = list(getattr(about, 'team', []) or [])

    try:
        offset = int(request.GET.get('offset', '0'))
    except ValueError:
        offset = 0
    offset = max(0, offset)

    page = team[offset:offset + TEAM_PAGE_SIZE]
    next_offset = offset + len(page)

    context = {
        'team': page,
        'has_more': next_offset < len(team),
        'next_offset': next_offset,
    }
    return render(request, 'django_starter/about/partials/team.html', context)


def partials_faq(request):
    """HTMX：分页返回更多 FAQ 条目。"""
    about = get_about()
    faqs = list(getattr(about, 'faqs', []) or [])

    try:
        offset = int(request.GET.get('offset', '0'))
    except ValueError:
        offset = 0
    offset = max(0, offset)

    page = faqs[offset:offset + FAQ_PAGE_SIZE]
    next_offset = offset + len(page)

    context = {
        'faqs': page,
        'has_more': next_offset < len(faqs),
        'next_offset': next_offset,
    }
    return render(request, 'django_starter/about/partials/faq.html', context)


def contact(request):
    """渲染并处理联系表单。"""
    about = get_about()
    contact_info = [
        {'icon': 'fa-solid fa-envelope', 'name': '邮箱', 'value': about.email},
        {'icon': 'fa-solid fa-phone', 'name': '电话', 'value': about.phone},
        {'icon': 'fa-solid fa-location-dot', 'name': '地址', 'value': about.address},
        {'icon': 'fa-solid fa-earth-americas', 'name': '网站', 'value': 'https://github.com/Deali-Axy/django-starter'},
        {'icon': 'fa-brands fa-x-twitter', 'name': 'X', 'value': 'https://x.com/DjangoStarter'},
        {'icon': 'fa-brands fa-facebook-f', 'name': 'Facebook', 'value': 'https://facebook.com/DjangoStarter'},
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
    """渲染隐私政策页面。"""
    return render(request, 'django_starter/about/privacy_policy.html')


def terms_of_service(request):
    """渲染服务条款页面。"""
    return render(request, 'django_starter/about/terms_of_service.html')
