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
    Year,
    Month,
    Shift,
    SalaryCalculation,
)


# Create your views here.


@login_required
def index_view(request):
    if request.method == "POST":
        form = SalaryCalculationForm(data=request.POST)
        if form.is_valid():
            group_name = form.cleaned_data["group_name"]
            year_month = form.cleaned_data["year_month"]
            extra_hour = form.cleaned_data["extra_hour"]
            bonus_percent = form.cleaned_data["bonus_percent"]
            monthly_salary = form.cleaned_data["monthly_salary"]

            salary = float(monthly_salary)
            overtime = extra_hour
            bonus_percent = bonus_percent

            user = request.user
            year = Year.objects.get(year_value=year_month.year)
            month = Month.objects.get(month_number=year_month.month)
            shift = Shift.objects.get(value=group_name)
            work_calendar = WorkCalendar.objects.filter(year=year, month=month).first()
            monthly_work_hour = work_calendar.monthly_work_hour
            
            if shift.value == "a":
                group_a_general_work_hour = work_calendar.group_a_general_work_hour
                group_a_daytime_work_hour = work_calendar.group_a_daytime_work_hour
                group_a_nighttime_work_hour = work_calendar.group_a_nighttime_work_hour
                group_a_holiday_work_hour = work_calendar.group_a_holiday_work_hour


                hourly_wage = round(float(salary) / float(group_a_general_work_hour), 2)
                night_work_pay = round(float(group_a_nighttime_work_hour) * float(hourly_wage) * 0.2, 2)
                extra_hour_pay = 0
                if group_a_general_work_hour - monthly_work_hour > 0:
                    extra_hour_pay = round((float(group_a_general_work_hour) - float(monthly_work_hour)) * float(hourly_wage) * 2, 2)
                holiday_hour_pay = 0
                if group_a_holiday_work_hour and group_a_holiday_work_hour > 0:
                    holiday_hour_pay = round(float(group_a_holiday_work_hour) * float(hourly_wage), 2)
                overtime_pay = 0
                if overtime and overtime > 0:
                    overtime_pay = round(float(overtime) * float(hourly_wage) * 2, 2)
                bonus_pay = 0
                if bonus_percent and bonus_percent > 0:
                    bonus_pay = round(float(salary) * float(bonus_percent) / 100, 2)
                gross = round(salary + night_work_pay + extra_hour_pay + holiday_hour_pay + overtime_pay + bonus_pay, 2)

                if gross <= 8000:
                    income_tax = 0
                else:
                    income_tax = round((float(gross) - 8000) * 0.14, 2)
                if gross <= 200:
                    dsmf_tax = round(gross * 0.03, 2)
                else:
                    dsmf_tax = round((float(gross) - 200) * 0.1 + 6, 2)
                if gross > 0:
                    unemployment_insurance_tax = round(gross * 0.005, 2)
                else:
                    unemployment_insurance_tax = 0
                if gross <= 8000:
                    compulsory_health_insurance_tax = round(gross * 0.02, 2)
                else:
                    compulsory_health_insurance_tax = round((float(gross) - 8000) * 0.005 + 160, 2)

                nett = round(gross - income_tax - dsmf_tax - unemployment_insurance_tax - compulsory_health_insurance_tax, 2)

                print(f"monthly_work_hour: {monthly_work_hour}")
                print(f"group_a_general_work_hour: {group_a_general_work_hour}")
                print(f"group_a_nighttime_work_hour: {group_a_nighttime_work_hour}")
                print(f"group_a_holiday_work_hour: {group_a_holiday_work_hour}")
                print(f"hourly_wage: {hourly_wage}")
                print(f"night_work_pay: {night_work_pay}")
                print(f"extra_hour_pay: {extra_hour_pay}")
                print(f"holiday_hour_pay: {holiday_hour_pay}")
                print(f"overtime_pay: {overtime_pay}")
                print(f"bonus_pay: {bonus_pay}")
                print(f"gross: {gross}")
                print(f"income_tax: {income_tax}")
                print(f"dsmf_tax: {dsmf_tax}")
                print(f"unemployment_insurance_tax: {unemployment_insurance_tax}")
                print(f"compulsory_health_insurance_tax: {compulsory_health_insurance_tax}")
                print(f"nett: {nett}")


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
