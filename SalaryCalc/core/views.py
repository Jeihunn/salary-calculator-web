from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .forms import (
    SalaryCalculationForm,
)
from .models import (
    WorkCalendar,
    Month,
)


# Create your views here.


@login_required
def index_view(request):
    if request.method == "POST":
        form = SalaryCalculationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            messages.success(request, _("Maaş hesablama ugurla tamamlandi."))
            return redirect(reverse_lazy("core:index_view"))
    else:
        form = SalaryCalculationForm()

    context = {
        "form": form,
    }
    return render(request, "core/index.html", context)


def work_calendar_view(request):
    years = WorkCalendar.get_years_list()
    months = Month.objects.all()
    work_calendar_data = WorkCalendar.get_work_calendar_data()

    context = {
        "years": years,
        "months": months,
        "work_calendar_data": work_calendar_data
    }
    return render(request, "core/work-calendar.html", context)
