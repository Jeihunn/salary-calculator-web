from django.urls import path, re_path
from allauth.account import views as allauth_views
from . import views

urlpatterns = [
    path("signup/", allauth_views.signup, name="account_signup"),
    path("login/", allauth_views.login, name="account_login"),
    path("logout/", allauth_views.logout, name="account_logout"),

    path("account/profile/", views.profile_view, name="profile_view"),

    # password change
    path(
        "account/password/change/",
        allauth_views.password_change,
        name="account_change_password",
    ),

    # confirm email
    path(
        "confirm-email/",
        allauth_views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        allauth_views.confirm_email,
        name="account_confirm_email",
    ),

    # password reset
    path(
        "password/reset/",
        allauth_views.password_reset,
        name="account_reset_password"),
    path(
        "password/reset/done/",
        allauth_views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        allauth_views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        allauth_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
]
