from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
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


def after_pay(req):
    return render(req, "payments/after_pay.html")
