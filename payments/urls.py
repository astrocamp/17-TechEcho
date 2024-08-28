# payments/urls.py

from django.urls import path
from .views import index, create_payment, confirm_payment, cancel_payment

urlpatterns = [
    path("", index, name="index"),  # This is the root of the payments app
    path("create/", create_payment, name="create_payment"),
    path("confirm/", confirm_payment, name="confirm_payment"),
    path("cancel/", cancel_payment, name="cancel_payment"),
]
