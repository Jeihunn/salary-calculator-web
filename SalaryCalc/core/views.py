from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import (
    WorkCalendar,
    Month,
)


# Create your views here.


@login_required
def index_view(request):
    return render(request, "core/index.html")


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
