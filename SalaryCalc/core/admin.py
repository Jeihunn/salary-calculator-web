from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags
from django.contrib import messages
from .models import (
    Year,
    Month,
    Shift,
    WorkCalendar,
    WorkCalendarImage,
    SalaryCalculation,
    FAQ,
)


# Register your models here.


# ===== Actions =====
def toggle_active_selected(modeladmin, request, queryset):
    count = queryset.count()
    for obj in queryset:
        obj.is_active = not obj.is_active
        obj.save()

    message = _(f"{count} obyektin aktivlik vəziyyəti uğurla dəyiştirildi.")
    modeladmin.message_user(request, message, level=messages.SUCCESS)


toggle_active_selected.short_description = _(
    "Seçilənlərin Aktivlik vəziyyətini dəyiştir")
# ===== END Actions =====


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
    actions = [toggle_active_selected]

    list_display = ["id", "user", "year", "month", "shift", "salary",
                    "gross", "nett", "is_active", "created_at", "updated_at"]
    list_display_links = ["id", "user"]
    list_filter = ["year", "month", "shift"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    actions = [toggle_active_selected]

    list_display = ["id", "question_short", "answer_short", "display_order",
                    "is_active"]
    list_display_links = ["id", "question_short"]
    list_filter = ["is_active"]
    search_fields = ["question", "answer"]
    ordering = ["display_order"]

    def question_short(self, obj):
        if obj.question:
            if len(strip_tags(obj.question)) > 100:
                return f"{strip_tags(obj.question)[:100]}..."
            else:
                return strip_tags(obj.question)
        return None
    question_short.short_description = _("Sual")

    def answer_short(self, obj):
        if obj.answer:
            if len(strip_tags(obj.answer)) > 100:
                return f"{strip_tags(obj.answer)[:100]}..."
            else:
                return strip_tags(obj.answer)
        return None
    answer_short.short_description = _("Cavab")
