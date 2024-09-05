import os
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from linepay import LinePayApi

from users.models import User

from .ecpay.create_order import ecpay_api
from .models import Payment


def index(request):
    return render(request, "payments/index.html")


def mentor(request):
    return render(request, "payments/mentor.html")


@login_required
def payment_option(request):
    username = request.user.username
    payment_user = get_object_or_404(User, username=username)
    print(f"{payment_user}")
    if payment_user.is_student:
        print(f"{payment_user} 已是付費學生")
        return render(request, "payments/after_pay.html", {"user_id": username})
    else:
        print(f"{payment_user} 還不是付費學生")
    return render(request, "payments/payment_option.html")


@login_required
def ecpay(request):
    username = request.user.username
    payment_user = get_object_or_404(User, username=username)
    print(f"{payment_user}")
    if payment_user.is_student:
        print(f"{payment_user} 已是付費學生")
        return render(request, "payments/after_pay.html", {"user_id": username})
    else:
        print(f"{payment_user} 還不是付費學生")
        return HttpResponse(ecpay_api(username))


@csrf_exempt
def ecpay_return(request):
    if request.method == "POST":
        result = request.POST
        user_id = request.POST.get("CustomField1")
        process_date = request.POST.get("process_date")
        amount = request.POST.get("amount")
        RtnMsg = request.POST.get("RtnMsg")
        print(f"{result}")
        print(f"付款用戶名:{user_id}")
        print(f"交易日期:{process_date}")
        print(f"交易金額:{amount}")
        print(f"交易結果:{RtnMsg}")

        User.objects.filter(username=user_id).update(is_student="True")
        return HttpResponse("Payment confirmed!")


@csrf_exempt
def after_pay(request):
    if request.method == "POST":
        result2 = request.POST
        user_id = request.POST.get("CustomField1")
        print(f"{result2}")
        return render(request, "payments/after_pay.html", {"user_id": user_id})


@login_required
def disable_premium(request):
    user_id = request.user.username
    User.objects.filter(username=user_id).update(is_student="False")


def linepay_create_payment(request):
    plan = request.GET.get("plan", "basic")

    # Set the amount based on the selected plan
    if plan == "premium":
        amount = 600  # Example amount for Premium VIP
    else:
        amount = 0  # Free for Basic plan

    currency = "TWD"
    order_id = str(uuid.uuid4())

    # Create payment object in your database
    payment = Payment.objects.create(
        order_id=order_id,
        amount=amount,
        currency=currency,
    )

    # Initialize the LINE Pay API client
    line_pay = LinePayApi(
        channel_id=os.getenv("LINE_PAY_CHANNEL_ID", "your_channel_id"),
        channel_secret=os.getenv("LINE_PAY_CHANNEL_SECRET", "your_channel_secret"),
        is_sandbox=True,  # Set to False for production
    )

    # Set up the payment request payload for LINE Pay
    payload = {
        "amount": amount,
        "currency": currency,
        "orderId": order_id,
        "packages": [
            {
                "id": "package_id",
                "amount": amount,
                "name": f"{plan.capitalize()} VIP Plan",
                "products": [
                    {
                        "name": f"TechEcho {plan.capitalize()} Plan",
                        "quantity": 1,
                        "price": amount,
                    }
                ],
            }
        ],
        "redirectUrls": {
            "confirmUrl": request.build_absolute_uri(
                reverse("payments:linepay_confirm_payment")
            ),
            "cancelUrl": request.build_absolute_uri(
                reverse("payments:linepay_cancel_payment")
            ),
        },
    }

    # Make the payment request using the SDK
    try:
        response = line_pay.request(payload)
        if response["returnCode"] == "0000":
            # Save transaction ID to the payment object
            payment.transaction_id = response["info"]["transactionId"]
            payment.save()

            # Redirect the user to the LINE Pay payment page
            return redirect(response["info"]["paymentUrl"]["web"])
        else:
            return render(
                request,
                "payments/payment_error.html",
                {"error": response["returnMessage"]},
            )
    except Exception as e:
        return render(request, "payments/payment_error.html", {"error": str(e)})


def linepay_confirm_payment(request):
    user_id = request.user.username
    print(f"{user_id}")
    User.objects.filter(username=user_id).update(is_student="True")
    return HttpResponse("Payment confirmed!")


def linepay_cancel_payment(request):
    return HttpResponse("Payment canceled!")
