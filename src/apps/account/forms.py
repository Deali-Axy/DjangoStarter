from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'gender', 'phone']
        labels = {
            'full_name': '姓名',
            'gender': '性别',
            'phone': '手机号',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'autocomplete': 'name',
            }),
            'gender': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'autocomplete': 'tel',
            }),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '请输入用户名',
            'autocomplete': 'username',
        }),
        min_length=4,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '请输入密码',
            'autocomplete': 'current-password',
        }),
        min_length=4,
    )


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'name@example.com',
            'autocomplete': 'email',
        }),
    )
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '请输入用户名',
            'autocomplete': 'username',
        }),
        min_length=4,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '请输入密码',
            'autocomplete': 'new-password',
            'x-model': 'pw',
        }),
        min_length=4,
    )
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '请输入确认密码',
            'autocomplete': 'new-password',
            'x-model': 'confirm',
        }),
        min_length=4,
    )
