from django import forms
import time
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.utils.translation import ugettext_lazy, ugettext as _

from django.contrib.auth import get_user_model

ERROR_MESSAGE = ugettext_lazy("Please enter the correct username and password "
                              "for a staff account. Note that both fields are case-sensitive.")

OVER_TIME=ugettext_lazy("您的账号已经过期，请联系管理员")  #自定义报错信息

class AdminAuthenticationForm(AuthenticationForm):    #账号登录的form
    """
    A custom authentication form used in the admin app.

    """
    this_is_the_login_form = forms.BooleanField(
        widget=forms.HiddenInput, initial=1,
        error_messages={'required': ugettext_lazy("Please log in again, because your session has expired.")})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        message = ERROR_MESSAGE
        if username and password:
            self.user_cache = authenticate(
                username=username, password=password)
            if self.user_cache is None:
                if u'@' in username:
                    User = get_user_model()
                    # Mistakenly entered e-mail address instead of username? Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your username."
                                        " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active or not self.user_cache.is_staff:
                raise forms.ValidationError(message)
            # 自定义功能 设置用户账号超时：
            elif self.user_cache.over_time and self.user_cache.over_time< time.time():
                raise forms.ValidationError(OVER_TIME)

        return self.cleaned_data
