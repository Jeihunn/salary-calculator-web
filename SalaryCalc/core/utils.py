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


def calculate_taxes(gross, year, union_membership_percent=0):
    try:
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

        taxes = {
            "income_tax": 0,
            "dsmf_tax": 0,
            "unemployment_insurance_tax": 0,
            "compulsory_health_insurance_tax": 0,
            "union_membership_tax": 0
        }

        if year in tax_rates_by_year:
            tax_rates = tax_rates_by_year[year]
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
                union_membership_percent = float(union_membership_percent)
                taxes["union_membership_tax"] = round(
                    gross * union_membership_percent / 100, 2)

                return taxes
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def gross_to_nett_for_year(gross, year, union_membership_percent):
    if gross > 0:
        taxes = calculate_taxes(gross, year, union_membership_percent)
        nett = round(gross - sum(taxes.values()), 2)

        return {"gross": gross, "nett": nett, "union_membership_percent": union_membership_percent, "taxes": taxes}
    else:
        return None


def calculate_gross_to_nett(gross, year=None, union_membership_percent=0):
    try:
        gross = float(gross)
        results = {}

        if year:
            # If a specific year is given, calculate only for that year
            results[year] = gross_to_nett_for_year(
                gross, year, union_membership_percent)
        else:
            # If year is not specified, calculate for all years from 2020 to 2024
            for year in range(2020, 2025):
                results[year] = gross_to_nett_for_year(
                    gross, year, union_membership_percent)
        return results
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def nett_to_gross_for_year(nett, year):
    if nett > 0:
        if year == 2020:
            if nett <= 193:
                gross = nett / 0.965
            elif nett > 193 and nett <= 7174:
                gross = (nett - 14) / 0.895
            else:
                gross = (nett - 1134) / 0.755
        elif year == 2021:
            if nett <= 191:
                gross = nett / 0.955
            elif nett > 191 and nett <= 7094:
                gross = (nett - 14) / 0.885
            else:
                gross = (nett - 1094) / 0.75
        elif year in range(2022, 2025):
            if nett <= 189:
                gross = nett / 0.945
            elif nett > 189 and nett <= 7014:
                gross = (nett - 14) / 0.875
            else:
                gross = (nett - 1014) / 0.75

        gross = round(gross, 2)
        taxes = calculate_taxes(gross, year)

        return {"nett": nett, "gross": gross, "taxes": taxes}
    else:
        return None


def calculate_nett_to_gross(nett, year=None):
    try:
        nett = float(nett)

        results = {}

        if year:
            # If a specific year is given, calculate only for that year
            results[year] = nett_to_gross_for_year(nett, year)
        else:
            # If year is not specified, calculate for all years from 2020 to 2024
            for year in range(2020, 2025):
                results[year] = nett_to_gross_for_year(nett, year)
        return results
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def calculate_hourly_wage(salary, work_hour):
    return salary / work_hour


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
            "hourly_wage": round(hourly_wage, 2),
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
            "compulsory_health_insurance_tax": nett_and_taxes[year.year_value]["taxes"]["compulsory_health_insurance_tax"]
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
