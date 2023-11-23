from django.urls import path
from . import views as api_views

app_name = "api_core"
urlpatterns = [
    path("subscriber/", api_views.SubscriberCreateAPIView.as_view(),
         name="api_subscriber_create_view"),
]