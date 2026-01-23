from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.forms import SignupForm as AllauthSignupForm


class LoginForm(AllauthLoginForm):
    """
    allauth 登录表单的样式适配（DaisyUI）。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "login" in self.fields:
            self.fields["login"].widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "autocomplete": "username",
                }
            )
        if "password" in self.fields:
            self.fields["password"].widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "autocomplete": "current-password",
                }
            )


class SignupForm(AllauthSignupForm):
    """
    allauth 注册表单的样式适配（DaisyUI）。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "email" in self.fields:
            self.fields["email"].widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "autocomplete": "email",
                    "placeholder": "name@example.com",
                }
            )
        if "username" in self.fields:
            self.fields["username"].widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "autocomplete": "username",
                }
            )
        if "password1" in self.fields:
            self.fields["password1"].widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "autocomplete": "new-password",
                }
            )
        if "password2" in self.fields:
            self.fields["password2"].widget.attrs.update(
                {
                    "class": "input input-bordered w-full",
                    "autocomplete": "new-password",
                }
            )
