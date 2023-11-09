from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("work-calendar", views.work_calendar_view, name="work_calendar_view"),
]
