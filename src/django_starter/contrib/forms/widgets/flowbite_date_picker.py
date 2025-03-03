from django import forms


class FlowbiteDatePickerWidget(forms.DateInput):
    template_name = 'django_starter/forms/widgets/flowbite_date_picker.html'

    def __init__(self, attrs=None, custom_class=''):
        final_attrs = {'class': custom_class}
        if attrs:
            final_attrs.update(attrs)
        super(FlowbiteDatePickerWidget, self).__init__(attrs=final_attrs)
