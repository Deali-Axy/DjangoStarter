# your_app/forms/base.py
from django import forms
from .mixins import BaseFormMixin


class BaseForm(BaseFormMixin, forms.Form):
    """普通Form的基类"""
    pass


class BaseModelForm(BaseFormMixin, forms.ModelForm):
    """ModelForm的基类"""
    pass
