from .models import (
    Year,
    Month,
    Shift,
    WorkCalendar
)


NIGHT_WORK_PAY_RATE = 0.2
EXTRA_HOUR_PAY_RATE = 2


def gross_to_nett_for_year(gross, year, tax_rates, union_membership_tax):
    taxes = {
        "income_tax": 0,
        "dsmf_tax": 0,
        "unemployment_insurance_tax": 0,
        "compulsory_health_insurance_tax": 0,
        "union_membership_tax": 0
    }

    if gross > 0:
        if gross <= 200:
            taxes["dsmf_tax"] = round(
                gross * tax_rates.get("dsmf_tax_1", 0), 2)
        else:
            taxes["dsmf_tax"] = round(
                (gross - 200) * tax_rates.get("dsmf_tax_2", 0) + 200 * tax_rates.get("dsmf_tax_1", 0), 2)

        if gross <= 8000:
            taxes["compulsory_health_insurance_tax"] = round(
                gross * tax_rates.get("compulsory_health_insurance_tax_1", 0), 2)
        else:
            taxes["compulsory_health_insurance_tax"] = round((gross - 8000) * tax_rates.get(
                "compulsory_health_insurance_tax_2", 0) + 8000 * tax_rates.get("compulsory_health_insurance_tax_1", 0), 2)
            taxes["income_tax"] = round(
                (gross - 8000) * tax_rates.get("income_tax", 0), 2)
        taxes["unemployment_insurance_tax"] = round(
            gross * tax_rates.get("unemployment_insurance_tax", 0), 2)
        taxes["union_membership_tax"] = round(
            gross * union_membership_tax / 100, 2)

    nett = round(gross - sum(taxes.values()), 2)

    return {"gross": gross, "nett": nett, "taxes": taxes}


def get_shift_variables(shift_value, work_calendar):
    if shift_value in ["a", "b", "c", "d"]:
        shift_fields = [
            f"group_{shift_value}_general_work_hour",
            f"group_{shift_value}_nighttime_work_hour",
            f"group_{shift_value}_holiday_work_hour"
        ]
        return [getattr(work_calendar, field) for field in shift_fields]
    return None


def calculate_gross_to_nett(gross, year=None, union_membership_tax=0):
    gross = float(gross)

    # Adjust tax rates by year
    tax_rates_by_year = {
        2020: {
            "income_tax": 0.14,
            "dsmf_tax_1": 0.03,
            "dsmf_tax_2": 0.1,
            "unemployment_insurance_tax": 0.005
        },
        2021: {
            "income_tax": 0.14,
            "dsmf_tax_1": 0.03,
            "dsmf_tax_2": 0.1,
            "unemployment_insurance_tax": 0.005,
            "compulsory_health_insurance_tax_1": 0.01,
            "compulsory_health_insurance_tax_2": 0.005
        },
        2022: {
            "income_tax": 0.14,
            "dsmf_tax_1": 0.03,
            "dsmf_tax_2": 0.1,
            "unemployment_insurance_tax": 0.005,
            "compulsory_health_insurance_tax_1": 0.02,
            "compulsory_health_insurance_tax_2": 0.005
        },
        2023: {
            "income_tax": 0.14,
            "dsmf_tax_1": 0.03,
            "dsmf_tax_2": 0.1,
            "unemployment_insurance_tax": 0.005,
            "compulsory_health_insurance_tax_1": 0.02,
            "compulsory_health_insurance_tax_2": 0.005
        },
        2024: {
            "income_tax": 0.14,
            "dsmf_tax_1": 0.03,
            "dsmf_tax_2": 0.1,
            "unemployment_insurance_tax": 0.005,
            "compulsory_health_insurance_tax_1": 0.02,
            "compulsory_health_insurance_tax_2": 0.005
        }
    }

    results = {}

    if year:
        # If a specific year is given, calculate only for that year
        if year in tax_rates_by_year:
            tax_rates = tax_rates_by_year[year]
            results[year] = gross_to_nett_for_year(
                gross, year, tax_rates, union_membership_tax)
    else:
        # If year is not specified, calculate for all years from 2020 to 2024
        for year in range(2020, 2025):
            tax_rates = tax_rates_by_year[year]
            results[year] = gross_to_nett_for_year
    return results


def calculate_hourly_wage(salary, work_hour):
    return round(salary / work_hour, 2)


def calculate_night_work_pay(nighttime_work_hour, hourly_wage):
    return round(nighttime_work_hour * hourly_wage * NIGHT_WORK_PAY_RATE, 2)


def calculate_extra_hour_pay(general_work_hour, monthly_work_hour, hourly_wage):
    extra_hours = max(0, general_work_hour - monthly_work_hour)
    return round(extra_hours * hourly_wage * EXTRA_HOUR_PAY_RATE, 2)


def calculate_holiday_hour_pay(holiday_work_hour, hourly_wage):
    return round(holiday_work_hour * hourly_wage, 2)


def calculate_overtime_pay(overtime, hourly_wage):
    return round(overtime * hourly_wage * EXTRA_HOUR_PAY_RATE, 2)


def calculate_bonus_pay(salary, bonus_percent):
    return round(salary * bonus_percent / 100, 2)


def calculate_salary(group_name, year_month, monthly_salary, overtime, bonus_percent):
    try:
        salary = float(monthly_salary)
        overtime = float(overtime)
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
            if holiday_work_hour is None:
                holiday_work_hour = 0

            hourly_wage = calculate_hourly_wage(salary, general_work_hour)
            night_work_pay = calculate_night_work_pay(
                nighttime_work_hour, hourly_wage)
            extra_hour_pay = calculate_extra_hour_pay(
                general_work_hour, monthly_work_hour, hourly_wage)
            holiday_hour_pay = calculate_holiday_hour_pay(
                holiday_work_hour, hourly_wage)
        elif shift.value == "g":
            hourly_wage = calculate_hourly_wage(salary, monthly_work_hour)
            night_work_pay = 0
            extra_hour_pay = 0
            holiday_hour_pay = 0

        overtime_pay = calculate_overtime_pay(overtime, hourly_wage)
        bonus_pay = calculate_bonus_pay(salary, bonus_percent)

        gross = round(salary + night_work_pay + extra_hour_pay +
                      holiday_hour_pay + overtime_pay + bonus_pay, 2)

        nett_and_taxes = calculate_gross_to_nett(gross, year.year_value)

        return {
            "year": year,
            "month": month,
            "shift": shift,
            "salary": salary,
            "overtime": overtime,
            "bonus_percent": bonus_percent,
            "hourly_wage": hourly_wage,
            "night_work_pay": night_work_pay,
            "extra_hour_pay": extra_hour_pay,
            "holiday_hour_pay": holiday_hour_pay,
            "overtime_pay": overtime_pay,
            "bonus_pay": bonus_pay,
            "gross": gross,
            "nett": nett_and_taxes[year.year_value]["nett"],
            "income_tax": nett_and_taxes[year.year_value]["taxes"]["income_tax"],
            "dsmf_tax": nett_and_taxes[year.year_value]["taxes"]["dsmf_tax"],
            "unemployment_insurance_tax": nett_and_taxes[year.year_value]["taxes"]["unemployment_insurance_tax"],
            "compulsory_health_insurance_tax": nett_and_taxes[year.year_value]["taxes"]["compulsory_health_insurance_tax"],
            "union_membership_tax": nett_and_taxes[year.year_value]["taxes"]["union_membership_tax"]
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
