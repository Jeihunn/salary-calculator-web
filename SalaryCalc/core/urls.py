from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("work-calendar", views.work_calendar_view, name="work_calendar_view"),
    path("gross-to-nett", views.groos_to_nett_view, name="groos_to_nett_view"),
    path("nett-to-gross", views.nett_to_gross_view, name="nett_to_gross_view"),
]
