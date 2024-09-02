from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.index, name="index"),
    path("mentor", views.mentor, name="mentor"),
    path("new", views.new, name="new"),
    path("payment_option", views.payment_option, name="payment_option"),
    path("ecpay", views.ecpay, name="ecpay"),
    path("linepay", views.ecpay, name="linepay"),
    path("after_pay", views.after_pay, name="after_pay"),
]
