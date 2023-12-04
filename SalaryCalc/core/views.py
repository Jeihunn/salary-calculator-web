from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .utils import (
    calculate_salary,
    calculate_gross_to_nett,
    calculate_nett_to_gross,
)
from .forms import (
    SalaryCalculationForm,
    GrossToNettForm,
    NettToGrossForm,
    ContactForm,
)
from .models import (
    WorkCalendar,
    Month,
    SalaryCalculation,
    FAQ,
    CalculationCount
)


# Create your views here.


@login_required
def index_view(request):
    if request.method == "POST":
        form = SalaryCalculationForm(data=request.POST)
        if form.is_valid():
            group_name = form.cleaned_data["group_name"]
            year_month = form.cleaned_data["year_month"]
            overtime = form.cleaned_data["overtime"] or 0
            bonus_percent = form.cleaned_data["bonus_percent"] or 0
            monthly_salary = form.cleaned_data["monthly_salary"]

            data = calculate_salary(
                group_name, year_month, monthly_salary, overtime, bonus_percent)

            if data:
                try:
                    SalaryCalculation.objects.create(
                        user=request.user,
                        year=data["year"],
                        month=data["month"],
                        shift=data["shift"],
                        salary=data["salary"],
                        overtime=data["overtime"],
                        bonus_percent=data["bonus_percent"],
                        hourly_wage=data["hourly_wage"],
                        night_work_pay=data["night_work_pay"],
                        extra_hour_pay=data["extra_hour_pay"],
                        holiday_hour_pay=data["holiday_hour_pay"],
                        overtime_pay=data["overtime_pay"],
                        bonus_pay=data["bonus_pay"],
                        gross=data["gross"],
                        nett=data["nett"],
                        income_tax=data["income_tax"],
                        dsmf_tax=data["dsmf_tax"],
                        unemployment_insurance_tax=data["unemployment_insurance_tax"],
                        compulsory_health_insurance_tax=data["compulsory_health_insurance_tax"]
                    )

                    calculation_count = CalculationCount.objects.first()
                    if calculation_count:
                        calculation_count.count += 1
                        calculation_count.save()
                    else:
                        CalculationCount.objects.create(count=1)

                    messages.success(request, _(
                        "Maaş hesablama uğurla tamamlandı."))
                    return redirect(reverse_lazy("core:index_view"))
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    messages.error(request, _(
                        "Maaş hesablanması zamanı xəta baş verdi. Zəhmət olmasa bir daha cəhd edin."))
                    return redirect(reverse_lazy("core:index_view"))
            else:
                messages.warning(request, _(
                    "Maaş hesablanması zamanı xəta baş verdi. Zəhmət olmasa bir daha cəhd edin. Əgər xəta təkrarlanarsa bizimlə əlaqə saxlayın."))
                print(f"An error occurred: {data}")
                return redirect(reverse_lazy("core:index_view"))
    else:
        form = SalaryCalculationForm()

    user_salary_calculations = SalaryCalculation.objects.filter(
        user=request.user, is_active=True).order_by("-created_at")[:10]

    # Retrieve corresponding WorkCalendar instances for each SalaryCalculation
    for calculation in user_salary_calculations:
        try:
            work_calendar = WorkCalendar.objects.get(
                year=calculation.year,
                month=calculation.month
            )
            calculation.nighttime_work_hour = getattr(
                work_calendar, f"group_{calculation.shift.value}_nighttime_work_hour", 0
            )
            calculation.holiday_work_hour = getattr(
                work_calendar, f"group_{calculation.shift.value}_holiday_work_hour", 0
            )

            monthly_work_hour = getattr(work_calendar, "monthly_work_hour", 0)
            general_work_hour = getattr(work_calendar, f"group_{calculation.shift.value}_general_work_hour", 0)
            calculation.extra_work_hour = max(0, general_work_hour - monthly_work_hour)
        except WorkCalendar.DoesNotExist:
            # Handle the case where WorkCalendar does not exist for the specified year and month
            calculation.nighttime_work_hour = None
            calculation.holiday_work_hour = None
            calculation.extra_work_hour = None
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    context = {
        "form": form,
        "user_salary_calculations": user_salary_calculations
    }
    return render(request, "core/index.html", context)


def groos_to_nett_view(request):
    data = None

    if request.method == "POST":
        form = GrossToNettForm(data=request.POST)
        if form.is_valid():
            gross = form.cleaned_data["gross"]
            union_membership_percent = form.cleaned_data["union_membership_percent"] or 0

            data = calculate_gross_to_nett(
                gross, union_membership_percent=union_membership_percent)

            if data:
                form = GrossToNettForm()

                calculation_count = CalculationCount.objects.first()
                if calculation_count:
                    calculation_count.count += 1
                    calculation_count.save()
                else:
                    CalculationCount.objects.create(count=1)

                messages.success(request, _("Hesablama tamamlandı."))
            else:
                messages.warning(request, _(
                    "Hesablama zamanı xəta baş verdi. Zəhmət olmasa bir daha cəhd edin."))
                return redirect(reverse_lazy("core:groos_to_nett_view"))
    else:
        form = GrossToNettForm()

    context = {
        "form": form,
        "data": data
    }
    return render(request, "core/gross-to-nett.html", context)


def nett_to_gross_view(request):
    data = None

    if request.method == "POST":
        form = NettToGrossForm(data=request.POST)
        if form.is_valid():
            nett = form.cleaned_data["nett"]

            data = calculate_nett_to_gross(nett)

            if data:
                form = NettToGrossForm()

                calculation_count = CalculationCount.objects.first()
                if calculation_count:
                    calculation_count.count += 1
                    calculation_count.save()
                else:
                    CalculationCount.objects.create(count=1)
                                    
                messages.success(request, _("Hesablama tamamlandı."))
            else:
                messages.warning(request, _(
                    "Hesablama zamanı xəta baş verdi. Zəhmət olmasa bir daha cəhd edin."))
                return redirect(reverse_lazy("core:nett_to_gross_view"))
    else:
        form = NettToGrossForm()

    context = {
        "form": form,
        "data": data
    }
    return render(request, "core/nett-to-gross.html", context)


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


def faq_view(request):
    faqs = FAQ.objects.filter(is_active=True).order_by("display_order")

    context = {
        "faqs": faqs,
    }
    return render(request, "core/faq.html", context)


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Mesaj uğurla göndərildi."))
            return redirect(reverse_lazy("core:contact_view"))
    else:
        form = ContactForm()

    context = {
        "form": form
    }
    return render(request, "core/contact.html", context)
