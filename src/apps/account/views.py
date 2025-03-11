from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import render, redirect, reverse

from .forms import UserProfileForm, RegisterForm, LoginForm


@login_required()
def index(request):
    return render(request, 'account/index.html')


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
    }
    return render(request, 'account/profile.html', ctx)


@login_required()
def charge(request):
    return render(request, 'account/charge.html')


@login_required()
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required()
def settings(request):
    return render(request, 'account/settings.html')


def login_view(request):
    next_url = request.GET.get('next', '')

    sso_redirect_url = reverse('account:login-sso')
    sso_redirect_url = request.build_absolute_uri(sso_redirect_url)
    ctx = {
        # 'sso_url': ids_lite.get_authorize_url(sso_redirect_url, state=next_url),
        'sso_url': '',
        'form': LoginForm(),
    }

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        if next_url:
            return redirect(next_url)
        else:
            return redirect(reverse('djs_guide:index'))

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

    userinfo = {
        'id': '',
        'phoneNumber': '',
        'userName': ''
    }

    if not code:
        messages.error(request, 'Invalid code.')
        return redirect(reverse('account:login'))

    try:
        userinfo = None
        # userinfo = ids_lite.get_user_info(code)
    except Exception as e:
        messages.error(request, f'SSO login failed. {e}')
        return redirect(reverse('account:login'))

    user_queryset: QuerySet[User] = User.objects.filter(username=userinfo['userName'])

    if user_queryset.exists():
        user = user_queryset.first()
    else:
        user: User = User.objects.create_user(
            username=userinfo['userName'],
        )
        user.profile.phone = userinfo['phoneNumber']
        user.profile.save()

    login(request, user)
    messages.success(request, f'Welcome {user.username}')
    if state:
        return redirect(state)
    else:
        return redirect(reverse('djs_guide:index'))


def signup_view(request):
    index_url = reverse('djs_guide:index')

    if request.user.is_authenticated:
        messages.warning(request, '您已经登录了，不用重复操作。')
        return redirect(index_url)

    form = RegisterForm()
    ctx = {'form': form}

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        ctx['form'] = form
        if not form.is_valid():
            return render(request, 'account/sign-up.html', ctx)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']

        if password != confirm_password:
            messages.error(request, '两次输入的密码不一致！')
            return render(request, 'account/sign-up.html', ctx)

        if User.objects.filter(username=username).exists():
            messages.warning(request, '用户名已存在。')
            return render(request, 'account/sign-up.html', ctx)

        user: User = User.objects.create_user(username=username, password=password)
        messages.success(request, f'注册成功！欢迎 {user.username}')
        login(request, user)
        return redirect(reverse('account:index'))

    return render(request, 'account/sign-up.html', ctx)


@login_required()
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect(reverse('djs_guide:index'))
