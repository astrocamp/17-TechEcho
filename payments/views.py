from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

from .ecpay.ecpay_create_order import main


# Create your views here.
def vip(req):
    pass


def new(req):
    pass


def index(req):
    return render(req, "payments/index.html")


def mentor(req):
    return render(req, "payments/mentor.html")


def payment_option(req):
    return render(req, "payments/payment_option.html")


def ecpay(req):
    return HttpResponse(main())


def linepay(req):
    pass


@csrf_exempt
def after_pay(req):
    return render(req, "payments/after_pay.html")
