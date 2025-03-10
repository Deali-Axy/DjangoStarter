from django import forms

from django_starter.contrib.about.models import Contact
from django_starter.contrib.forms import BaseForm, BaseModelForm


class ContactModelForm(BaseModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '请输入您的姓名'}),
            'email': forms.EmailInput(attrs={'placeholder': '请输入您的邮箱'}),
            'phone': forms.TextInput(attrs={'placeholder': '请输入您的联系电话'}),
            'message': forms.Textarea(attrs={'placeholder': '请输入您的留言内容', 'rows': 4})
        }
