from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt

from .ecpay.ecpay_create_order import main


# Create your views here.
def vip(request):
    pass


def new(request):
    pass


def index(request):
    return render(request, "payments/index.html")


def mentor(request):
    return render(request, "payments/mentor.html")


def payment_option(request):
    return render(request, "payments/payment_option.html")


def ecpay(request):
    return HttpResponse(main())


def linepay(request):
    pass


@csrf_exempt
def after_pay(request):
    return render(request, "payments/after_pay.html")
