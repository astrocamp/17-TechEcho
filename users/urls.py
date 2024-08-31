from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/<int:id>/", views.log_in, name="login"),
    path("login/", views.log_in, name="login_no_id"),
    path("<int:id>/logout", views.log_out, name="logout"),
    path("register/", views.register, name="register"),
    path("register/", views.register, name="register_no_id"),
]
