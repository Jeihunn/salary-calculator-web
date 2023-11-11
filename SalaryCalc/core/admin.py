from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Year,
    Month,
    Shift,
    WorkCalendar,
    WorkCalendarImage,
    SalaryCalculation
)


# Register your models here.


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ["id", "year_value", "created_at", "updated_at"]
    list_display_links = ["id", "year_value"]
    search_fields = ["year_value"]


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "month_number", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "value", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


@admin.register(WorkCalendar)
class WorkCalendarAdmin(admin.ModelAdmin):
    list_display = ["id", "year", "month", "monthly_work_hour", "group_a_general_work_hour",
                    "group_b_general_work_hour", "group_c_general_work_hour", "group_d_general_work_hour",]
    list_display_links = ["id", "year", "month"]
    list_filter = ["year", "month"]

    fieldsets = (
        (None, {
            'fields': (
                'year',
                'month',
                'monthly_work_hour',
            ),
        }),
        (_('Qrup A'), {
            'fields': (
                'group_a_general_work_hour',
                'group_a_daytime_work_hour',
                'group_a_nighttime_work_hour',
                'group_a_holiday_work_hour',
            ),
        }),
        (_('Qrup B'), {
            'fields': (
                'group_b_general_work_hour',
                'group_b_daytime_work_hour',
                'group_b_nighttime_work_hour',
                'group_b_holiday_work_hour',
            ),
        }),
        (_('Qrup C'), {
            'fields': (
                'group_c_general_work_hour',
                'group_c_daytime_work_hour',
                'group_c_nighttime_work_hour',
                'group_c_holiday_work_hour',
            ),
        }),
        (_('Qrup D'), {
            'fields': (
                'group_d_general_work_hour',
                'group_d_daytime_work_hour',
                'group_d_nighttime_work_hour',
                'group_d_holiday_work_hour',
            ),
        }),
    )


@admin.register(WorkCalendarImage)
class WorkCalendarImageAdmin(admin.ModelAdmin):
    list_display = ["id", "year", "image", "created_at", "updated_at"]
    list_display_links = ["id", "year"]
    list_filter = ["year"]


@admin.register(SalaryCalculation)
class SalaryCalculationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "year", "month", "shift", "salary", "gross", "nett", "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "user"]
    list_filter = ["year", "month", "shift"]