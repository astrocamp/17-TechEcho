import uuid

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from linepay import LinePayApi

from .models import Payment


def index(request):
    return render(request, "payments/index.html")


def create_payment(request):
    plan = request.GET.get("plan", "basic")

    # Set the amount based on the selected plan
    if plan == "premium":
        amount = 100  # Example amount for Premium VIP
    elif plan == "platinum":
        amount = 200  # Example amount for Platinum VIP
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
        channel_id=settings.LINE_PAY_CHANNEL_ID,
        channel_secret=settings.LINE_PAY_CHANNEL_SECRET,
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
                        "name": f"{plan.capitalize()} VIP Plan",
                        "quantity": 1,
                        "price": amount,
                    }
                ],
            }
        ],
        "redirectUrls": {
            "confirmUrl": request.build_absolute_uri(reverse("confirm_payment")),
            "cancelUrl": request.build_absolute_uri(reverse("cancel_payment")),
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


def confirm_payment(request):
    return HttpResponse("Payment confirmed!")


def cancel_payment(request):
    return HttpResponse("Payment canceled!")
