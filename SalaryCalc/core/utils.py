from .models import (
    Year,
    Month,
    Shift,
    WorkCalendar
)


NIGHT_WORK_PAY_RATE = 0.2
EXTRA_HOUR_PAY_RATE = 2


def get_shift_variables(shift_value, work_calendar):
    if shift_value in ["a", "b", "c", "d"]:
        shift_fields = [
            f"group_{shift_value}_general_work_hour",
            f"group_{shift_value}_nighttime_work_hour",
            f"group_{shift_value}_holiday_work_hour"
        ]
        return [getattr(work_calendar, field) for field in shift_fields]
    return None


def calculate_gross_to_nett(gross):
    gross = float(gross)

    tax_rates = {
        "income_tax": 0.14,
        "dsmf_tax_1": 0.03,
        "dsmf_tax_2": 0.1,
        "unemployment_insurance_tax": 0.005,
        "compulsory_health_insurance_tax_1": 0.02,
        "compulsory_health_insurance_tax_2": 0.005
    }

    taxes = {
        "income_tax": 0,
        "dsmf_tax": 0,
        "unemployment_insurance_tax": 0,
        "compulsory_health_insurance_tax": 0
    }

    if gross > 0:
        if gross <= 200:
            taxes["dsmf_tax"] = round(gross * tax_rates["dsmf_tax_1"], 2)
        else:
            taxes["dsmf_tax"] = round(
                (gross - 200) * tax_rates["dsmf_tax_2"] + 6, 2)

        if gross <= 8000:
            taxes["compulsory_health_insurance_tax"] = round(
                gross * tax_rates["compulsory_health_insurance_tax_1"], 2)
        else:
            taxes["compulsory_health_insurance_tax"] = round(
                (gross - 8000) * tax_rates["compulsory_health_insurance_tax_2"] + 160, 2)
            taxes["income_tax"] = round(
                (gross - 8000) * tax_rates["income_tax"], 2)
        taxes["unemployment_insurance_tax"] = round(
            gross * tax_rates["unemployment_insurance_tax"], 2)

    nett = round(gross - sum(taxes.values()), 2)

    return taxes["income_tax"], taxes["dsmf_tax"], taxes["unemployment_insurance_tax"], taxes["compulsory_health_insurance_tax"], nett


def calculate_salary(group_name, year_month, extra_hour, bonus_percent, monthly_salary):
    try:
        salary = float(monthly_salary)
        overtime = float(extra_hour)
        bonus_percent = float(bonus_percent)

        shift = Shift.objects.filter(value=group_name).first()
        year = Year.objects.filter(year_value=year_month.year).first()
        month = Month.objects.filter(month_number=year_month.month).first()
        work_calendar = WorkCalendar.objects.filter(
            year=year, month=month).first()

        monthly_work_hour = work_calendar.monthly_work_hour

        if shift.value in ["a", "b", "c", "d"]:
            general_work_hour, nighttime_work_hour, holiday_work_hour = get_shift_variables(
                shift.value, work_calendar)

            hourly_wage = round(salary / general_work_hour, 2)
            night_work_pay = round(nighttime_work_hour *
                                   hourly_wage * NIGHT_WORK_PAY_RATE, 2)
            extra_hour_pay = max(
                0, (general_work_hour - monthly_work_hour) * hourly_wage * EXTRA_HOUR_PAY_RATE)

            if holiday_work_hour and holiday_work_hour > 0:
                holiday_hour_pay = round(holiday_work_hour * hourly_wage, 2)
            else:
                holiday_hour_pay = 0
        elif shift.value == "g":
            hourly_wage = round(salary / monthly_work_hour, 2)
            night_work_pay = 0
            extra_hour_pay = 0
            holiday_hour_pay = 0

        if overtime and overtime > 0:
            overtime_pay = round(overtime * hourly_wage *
                                 EXTRA_HOUR_PAY_RATE, 2)
        else:
            overtime_pay = 0

        if bonus_percent and bonus_percent > 0:
            bonus_pay = round(salary * bonus_percent / 100, 2)
        else:
            bonus_pay = 0

        gross = round(salary + night_work_pay + extra_hour_pay +
                      holiday_hour_pay + overtime_pay + bonus_pay, 2)

        income_tax, dsmf_tax, unemployment_insurance_tax, compulsory_health_insurance_tax, nett = calculate_gross_to_nett(
            gross)

        return year, month, shift, salary, overtime, bonus_percent, hourly_wage, night_work_pay, extra_hour_pay, holiday_hour_pay, overtime_pay, bonus_pay, gross, nett, income_tax, dsmf_tax, unemployment_insurance_tax, compulsory_health_insurance_tax
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
