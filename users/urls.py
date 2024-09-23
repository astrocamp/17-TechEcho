from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("register/", views.register, name="register"),
    path("forget-password/", views.forget_password, name="forget_password"),
    path(
        "change-password/<uuid:token>/", views.change_password, name="change_password"
    ),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("public/profile/<int:id>/", views.public_profile, name="public_profile"),
    path(
        "public/profile/edit/<int:id>/",
        views.public_profile_edit,
        name="public_profile_edit",
    ),
]
