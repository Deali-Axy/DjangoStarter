# your_app/forms/mixins.py
from django import forms
from .widget_classes import *


class BaseFormMixin:
    """提供表单样式的通用混入类"""

    widget_classes = {
        forms.TextInput: TEXT_INPUT_CLASS,
        forms.Textarea: TEXT_AREA_CLASS,
        forms.EmailInput: TEXT_INPUT_CLASS,
        forms.PasswordInput: PASSWORD_INPUT_CLASS,
        forms.Select: SELECT_CLASS,
        forms.DateInput: DATE_INPUT_CLASS,
        forms.NumberInput: NUMBER_INPUT_CLASS,
    }

    def apply_widget_classes(self):
        """根据widget类型为表单字段应用样式"""
        for field_name, field in self.fields.items():
            widget_class = self.widget_classes.get(type(field.widget))
            if widget_class:
                field.widget.attrs.update({'class': widget_class})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widget_classes()
