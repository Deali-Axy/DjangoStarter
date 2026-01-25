from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.contrib.sessions.models import Session

from .forms import UserProfileForm, RegisterForm, LoginForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken

import base64
from io import BytesIO

import qrcode

from django_starter.contrib.auth.services import generate_token

from apps.billing.models import Wallet, TopUp, Subscription


def get_template_base(request):
    """
    Determine the base template based on whether the request is an HTMX request.
    """
    if request.headers.get('HX-Request'):
        return 'account/_account_partial.html'
    return 'account/_account_shell.html'


@login_required()
def index(request):
    return render(request, 'account/index.html', {
        'title': '用户中心',
        'base_template': get_template_base(request),
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '用户中心', 'url': None, 'icon': 'fa-solid fa-user'},
        ]
    })


@login_required()
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            user_profile = form.save()
            messages.info(request, f'Your profile has been updated!')
    else:
        form = UserProfileForm(instance=request.user.profile)

    ctx = {
        'form': form,
        'title': '个人资料',
        'base_template': get_template_base(request),
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '用户中心', 'url': reverse('account:index'), 'icon': 'fa-solid fa-user'},
            {'text': '个人资料', 'url': None, 'icon': 'fa-solid fa-id-card'},
        ]
    }
    return render(request, 'account/profile.html', ctx)


@login_required()
def charge(request):
    wallet, _created = Wallet.objects.get_or_create(user=request.user, currency='CNY')
    current_subscription = (
        Subscription.objects.filter(user=request.user, is_current=True)
        .select_related('plan')
        .first()
    )
    topups = (
        TopUp.objects.filter(user=request.user)
        .select_related('wallet')
        .order_by('-id')[:20]
    )
    return render(request, 'account/charge.html', {
        'title': '充值',
        'base_template': get_template_base(request),
        'wallet': wallet,
        'current_subscription': current_subscription,
        'topups': topups,
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '用户中心', 'url': reverse('account:index'), 'icon': 'fa-solid fa-user'},
            {'text': '充值', 'url': None, 'icon': 'fa-solid fa-wallet'},
        ]
    })


@login_required()
def dashboard(request):
    return render(request, 'account/dashboard.html', {
        'title': '仪表盘',
        'base_template': get_template_base(request),
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '用户中心', 'url': reverse('account:index'), 'icon': 'fa-solid fa-user'},
            {'text': '仪表盘', 'url': None, 'icon': 'fa-solid fa-gauge'},
        ]
    })


@login_required()
def settings(request):
    """
    账户设置中心。

    当前版本涵盖：
    - 修改密码
    - 会话管理（查看当前账号的活跃会话，支持退出其它设备/全部退出）
    """

    def _get_user_sessions(user: User) -> list[dict]:
        sessions = []
        for session in Session.objects.filter(expire_date__gt=timezone.now()):
            data = session.get_decoded()
            user_id = data.get('_auth_user_id')
            if str(user_id) != str(user.id):
                continue
            sessions.append({
                'session_key': session.session_key,
                'expire_date': session.expire_date,
                'is_current': session.session_key == request.session.session_key,
            })
        sessions.sort(key=lambda x: (not x['is_current'], x['expire_date']))
        return sessions

    password_form = PasswordChangeForm(user=request.user)
    for _name, field in password_form.fields.items():
        field.widget.attrs['class'] = 'input input-bordered w-full'

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'change_password':
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            for _name, field in password_form.fields.items():
                field.widget.attrs['class'] = 'input input-bordered w-full'
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, '密码修改成功。')
                return redirect(reverse('account:settings'))
            else:
                messages.error(request, '请检查输入项后重试。')

        if action in {'logout_others', 'logout_all'}:
            current_key = request.session.session_key
            target_sessions = []
            for session in Session.objects.filter(expire_date__gt=timezone.now()):
                data = session.get_decoded()
                if str(data.get('_auth_user_id')) != str(request.user.id):
                    continue
                target_sessions.append(session)

            if action == 'logout_others':
                target_sessions = [s for s in target_sessions if s.session_key != current_key]

            for s in target_sessions:
                s.delete()

            if action == 'logout_all':
                logout(request)
                messages.info(request, '已退出所有设备。请重新登录。')
                return redirect(reverse('account:login'))

            messages.success(request, '已退出其它设备。')
            return redirect(reverse('account:settings'))

    ctx = {
        'title': '设置',
        'base_template': get_template_base(request),
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '用户中心', 'url': reverse('account:index'), 'icon': 'fa-solid fa-user'},
            {'text': '设置', 'url': None, 'icon': 'fa-solid fa-gear'},
        ],
        'password_form': password_form,
        'sessions': _get_user_sessions(request.user),
        'is_2fa_enabled': TOTPDevice.objects.filter(user=request.user, confirmed=True).exists(),
    }
    return render(request, 'account/settings.html', ctx)


@login_required()
def settings_developer(request: HttpRequest) -> HttpResponse:
    ctx = {
        'title': 'Developer / API',
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '用户中心', 'url': reverse('account:index'), 'icon': 'fa-solid fa-user'},
            {'text': '设置', 'url': reverse('account:settings'), 'icon': 'fa-solid fa-gear'},
            {'text': 'Developer / API', 'url': None, 'icon': 'fa-solid fa-code'},
        ],
    }
    return render(request, 'account/settings/developer.html', ctx)


@login_required()
def settings_developer_token(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return redirect(reverse('account:settings-developer'))

    password = request.POST.get('password') or ''
    user = authenticate(request, username=request.user.username, password=password)
    if not user:
        messages.error(request, '密码不正确。')
        return render(request, 'account/settings/_developer_token.html', {'token': None})

    token_payload = generate_token({'username': user.username}).dict()
    return render(request, 'account/settings/_developer_token.html', {'token': token_payload})


def login_view(request):
    next_url = request.GET.get('next', '')

    sso_redirect_url = reverse('account:login-sso')
    sso_redirect_url = request.build_absolute_uri(sso_redirect_url)
    ctx = {
        # 'sso_url': ids_lite.get_authorize_url(sso_redirect_url, state=next_url),
        'sso_url': '',
        'form': LoginForm(),
        'title': '登录',
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '登录', 'url': None, 'icon': 'fa-solid fa-right-to-bracket'},
        ]
    }

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(reverse('home:index'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if not user:
                messages.warning(request, 'Invalid username or password.')
                return render(request, 'account/login.html', ctx)
            else:
                if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
                    request.session['pre_2fa_user_id'] = user.id
                    request.session['pre_2fa_next'] = next_url or reverse('account:index')
                    if hasattr(user, 'backend'):
                        request.session['pre_2fa_backend'] = user.backend
                    return redirect(reverse('account:2fa-verify'))

                messages.success(request, f'Welcome {user.username}')
                login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(reverse('account:index'))
        else:
            messages.error(request, '请输入有效的用户名和密码（至少4个字符）')

    return render(request, 'account/login.html', ctx)


def login_sso(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)

    if not code:
        messages.error(request, 'Invalid code.')
        return redirect(reverse('account:login'))

    try:
        userinfo = None
        # userinfo = ids_lite.get_user_info(code)
    except Exception as e:
        messages.error(request, f'SSO login failed. {e}')
        return redirect(reverse('account:login'))

    if not userinfo or not userinfo.get('userName'):
        messages.error(request, 'SSO 暂未启用或用户信息获取失败。')
        return redirect(reverse('account:login'))

    user_queryset: QuerySet[User] = User.objects.filter(username=userinfo['userName'])

    if user_queryset.exists():
        user = user_queryset.first()
    else:
        user: User = User.objects.create_user(
            username=userinfo['userName'],
        )
        user.profile.phone = userinfo.get('phoneNumber') or ''
        user.profile.save()

    login(request, user)
    messages.success(request, f'Welcome {user.username}')
    if state:
        return redirect(state)
    else:
        return redirect(reverse('home:index'))


def signup_view(request):
    index_url = reverse('home:index')

    if request.user.is_authenticated:
        messages.warning(request, '您已经登录了，不用重复操作。')
        return redirect(index_url)

    form = RegisterForm()
    ctx = {
        'form': form,
        'title': '注册',
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '注册', 'url': None, 'icon': 'fa-solid fa-user-plus'},
        ]
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        ctx['form'] = form
        if not form.is_valid():
            return render(request, 'account/signup.html', ctx)

        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        if password != confirm_password:
            messages.error(request, '两次输入的密码不一致！')
            return render(request, 'account/signup.html', ctx)

        if User.objects.filter(username=username).exists():
            messages.warning(request, '用户名已存在。')
            return render(request, 'account/signup.html', ctx)

        if User.objects.filter(email=email).exists():
            messages.warning(request, '邮箱已存在。')
            return render(request, 'account/signup.html', ctx)

        user: User = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, f'注册成功！欢迎 {user.username}')
        login(request, user)
        return redirect(reverse('account:index'))

    return render(request, 'account/signup.html', ctx)


@login_required()
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect(reverse('home:index'))


def _qr_data_uri(content: str) -> str:
    img = qrcode.make(content)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{data}'


def _verify_otp_token(user: User, token: str) -> bool:
    for device in TOTPDevice.objects.filter(user=user, confirmed=True):
        if device.verify_token(token):
            return True

    for device in StaticDevice.objects.filter(user=user, confirmed=True):
        if device.verify_token(token):
            return True

    return False


@login_required()
def two_factor_setup(request: HttpRequest) -> HttpResponse:
    if TOTPDevice.objects.filter(user=request.user, confirmed=True).exists():
        messages.info(request, '双因素认证已启用。')
        return redirect(reverse('account:settings'))

    device, _ = TOTPDevice.objects.get_or_create(
        user=request.user,
        name='default',
        defaults={'confirmed': False},
    )

    if request.method == 'POST':
        token = (request.POST.get('token') or '').strip().replace(' ', '')
        if not token:
            messages.error(request, '请输入验证码。')
        elif device.verify_token(token):
            device.confirmed = True
            device.save()

            static_device, _ = StaticDevice.objects.get_or_create(
                user=request.user,
                name='recovery',
                defaults={'confirmed': True},
            )
            static_device.confirmed = True
            static_device.save()

            StaticToken.objects.filter(device=static_device).delete()
            recovery_codes: list[str] = []
            for _i in range(10):
                code = StaticToken.random_token()
                StaticToken.objects.create(device=static_device, token=code)
                recovery_codes.append(code)

            return render(request, 'account/2fa/setup.html', {
                'title': '启用双因素认证',
                'base_template': get_template_base(request),
                'qr_data_uri': _qr_data_uri(device.config_url),
                'secret': device.key,
                'recovery_codes': recovery_codes,
                'breadcrumbs': [
                    {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
                    {'text': '用户中心', 'url': reverse('account:index'), 'icon': 'fa-solid fa-user'},
                    {'text': '设置', 'url': reverse('account:settings'), 'icon': 'fa-solid fa-gear'},
                    {'text': '启用双因素认证', 'url': None, 'icon': 'fa-solid fa-shield-halved'},
                ],
            })

        else:
            messages.error(request, '验证码无效，请重试。')

    return render(request, 'account/2fa/setup.html', {
        'title': '启用双因素认证',
        'base_template': get_template_base(request),
        'qr_data_uri': _qr_data_uri(device.config_url),
        'secret': device.key,
        'recovery_codes': None,
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '用户中心', 'url': reverse('account:index'), 'icon': 'fa-solid fa-user'},
            {'text': '设置', 'url': reverse('account:settings'), 'icon': 'fa-solid fa-gear'},
            {'text': '启用双因素认证', 'url': None, 'icon': 'fa-solid fa-shield-halved'},
        ],
    })


def two_factor_verify(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(reverse('account:index'))

    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        messages.warning(request, '请先登录。')
        return redirect(reverse('account:login'))

    next_url = request.session.get('pre_2fa_next') or reverse('account:index')
    backend = request.session.get('pre_2fa_backend')
    user = User.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, '用户不存在，请重新登录。')
        request.session.pop('pre_2fa_user_id', None)
        request.session.pop('pre_2fa_next', None)
        request.session.pop('pre_2fa_backend', None)
        return redirect(reverse('account:login'))

    if request.method == 'POST':
        token = (request.POST.get('token') or '').strip().replace(' ', '')
        if _verify_otp_token(user, token):
            request.session.pop('pre_2fa_user_id', None)
            request.session.pop('pre_2fa_next', None)
            request.session.pop('pre_2fa_backend', None)

            if backend:
                login(request, user, backend=backend)
            else:
                login(request, user)

            messages.success(request, '验证成功。')
            return redirect(next_url)
        else:
            messages.error(request, '验证码无效或已使用。')

    return render(request, 'account/2fa/verify.html', {
        'title': '双因素认证验证',
        'next': next_url,
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '登录验证', 'url': None, 'icon': 'fa-solid fa-shield-halved'},
        ],
    })


@login_required()
def two_factor_disable(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        password = request.POST.get('password') or ''
        token = (request.POST.get('token') or '').strip().replace(' ', '')

        if not request.user.check_password(password):
            messages.error(request, '密码不正确。')
        elif not _verify_otp_token(request.user, token):
            messages.error(request, '验证码无效或已使用。')
        else:
            TOTPDevice.objects.filter(user=request.user).delete()
            StaticDevice.objects.filter(user=request.user).delete()
            messages.success(request, '双因素认证已关闭。')
            return redirect(reverse('account:settings'))

    return render(request, 'account/2fa/disable.html', {
        'title': '关闭双因素认证',
        'base_template': get_template_base(request),
        'breadcrumbs': [
            {'text': '主页', 'url': reverse('home:index'), 'icon': 'fa-solid fa-home'},
            {'text': '用户中心', 'url': reverse('account:index'), 'icon': 'fa-solid fa-user'},
            {'text': '设置', 'url': reverse('account:settings'), 'icon': 'fa-solid fa-gear'},
            {'text': '关闭双因素认证', 'url': None, 'icon': 'fa-solid fa-shield-halved'},
        ],
    })
