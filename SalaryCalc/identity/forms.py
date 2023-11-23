from django import forms
from allauth.account.forms import SignupForm
from .models import Blacklist
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


# ========== Admin Forms ==========
class BlacklistAdminForm(forms.ModelForm):
    class Meta:
        model = Blacklist
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        ip_address = cleaned_data.get('ip_address')

        if not user and not ip_address:
            raise forms.ValidationError({
                'user': [_("Həm İstifadəçi, həm də IP ünvanı sahələri eyni vaxtda boş qala bilməz. Lütfən, ya İstifadəçi seçin, ya da IP ünvanı göstərin.")],
                'ip_address': [_("Həm İstifadəçi, həm də IP ünvanı sahələri eyni vaxtda boş qala bilməz. Lütfən, ya İstifadəçi seçin, ya da IP ünvanı göstərin.")]
            })

        if user and ip_address:
            raise forms.ValidationError({
                'user': [_("Siz eyni anda həm İstifadəçi seçə, həm də IP ünvanını təqdim edə bilməzsiniz. Lütfən, ya İstifadəçi seçin, ya da IP ünvanı göstərin.")],
                'ip_address': [_("Siz eyni anda həm İstifadəçi seçə, həm də IP ünvanını təqdim edə bilməzsiniz. Lütfən, ya İstifadəçi seçin, ya da IP ünvanı göstərin.")]
            })
# ========== END Admin Forms ==========


class CustomSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('Bu e-poçt ünvanı artıq qeydiyyatdan keçib.'))
        return email
