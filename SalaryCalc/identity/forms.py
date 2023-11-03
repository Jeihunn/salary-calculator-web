from django import forms
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('Bu e-poçt ünvanı artıq qeydiyyatdan keçib.'))
        return email
