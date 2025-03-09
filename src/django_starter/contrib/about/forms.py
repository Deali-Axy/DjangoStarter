from django import forms

from django_starter.contrib.about.models import Contact
from django_starter.contrib.forms import BaseForm, BaseModelForm


class ContactModelForm(BaseModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'message')


class ContactForm(BaseForm):
    name = forms.CharField(
        label='姓名',
        max_length=100,
        help_text='请输入您的姓名',
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'placeholder': '请输入您的姓名'
        }),
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'placeholder': '请输入您的邮箱'
        })
    )
    phone = forms.CharField(
        label='电话',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'placeholder': '请输入您的联系电话'
        })
    )
    message = forms.CharField(
        label='留言',
        widget=forms.Textarea(attrs={
            # 'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-4 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'placeholder': '请输入您的留言内容',
            'rows': 4
        })
    )
