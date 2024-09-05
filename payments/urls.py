from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.index, name="index"),
    path("mentor/", views.mentor, name="mentor"),
    path("payment_option/", views.payment_option, name="payment_option"),
    path("ecpay/", views.ecpay, name="ecpay"),
    path("ecpay_return/", views.ecpay_return, name="ecpay_return"),
    path("after_pay/", views.after_pay, name="after_pay"),
    path("disable_premium/", views.disable_premium, name="disable_premium"),
    path(
        "linepay_create/", views.linepay_create_payment, name="linepay_create_payment"
    ),
    path(
        "linepay_confirm/",
        views.linepay_confirm_payment,
        name="linepay_confirm_payment",
    ),
    path(
        "linepay_cancel/", views.linepay_cancel_payment, name="linepay_cancel_payment"
    ),
]
