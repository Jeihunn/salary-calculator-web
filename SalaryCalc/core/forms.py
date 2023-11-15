from django import forms
from datetime import date
from core.models import WorkCalendar
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import (
    Contact,
)


class SalaryCalculationForm(forms.Form):
    GROUP_CHOICES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
        ('g', 'Gündəlik'),
    ]

    years = WorkCalendar.get_years_list()
    if years:
        years_min = min(years)
        years_max = max(years)
    else:
        years_min = years_max = date.today().year

    group_name = forms.ChoiceField(
        choices=GROUP_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='a',
    )
    year_month = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'month',
            'class': 'form-control',
            'min': f'{years_min}-01',
            'max': f'{years_max}-12'
        }),
        input_formats=['%Y-%m']
    )
    overtime = forms.DecimalField(
        min_value=0,
        max_digits=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )
    bonus_percent = forms.DecimalField(
        min_value=0,
        max_value=500,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )
    monthly_salary = forms.DecimalField(
        min_value=1,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}),
    )

    def clean_year_month(self):
        year_month = self.cleaned_data['year_month']

        min_value = date(self.years_min, 1, 1)
        max_value = date(self.years_max, 12, 1)

        if not (min_value <= year_month <= max_value):
            raise ValidationError(
                _('İl və ay %(min)s və %(max)s arasında olmalıdır'),
                params={'min': min_value.strftime(
                    '%Y-%m'), 'max': max_value.strftime('%Y-%m')},
            )

        return year_month


class GrossToNettForm(forms.Form):
    gross = forms.DecimalField(
        min_value=1,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}),
    )
    union_membership_percent = forms.DecimalField(
        min_value=0,
        max_value=20,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )


class NettToGrossForm(forms.Form):
    nett = forms.DecimalField(
        min_value=1,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={'class': 'form-control'}),
    )


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ad Soyad'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'E-poçt'}),
            'subject': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Mövzu'}),
            'message': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Mesaj'}),
        }
