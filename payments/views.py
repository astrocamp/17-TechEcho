import base64
import hashlib
import hmac
import json
import os
import secrets
import uuid
from datetime import datetime

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from linepay import LinePayApi

from payments.ecpay import payment_sdk
from payments.ecpay.payment_sdk import ECPayPaymentSdk
from users.models import User

from .ecpay.create_order import ecpay_api
from .models import Order


###  General
def index(request):
    return render(request, "payments/index.html")


def check_premium_status(user):
    payment_user = get_object_or_404(User, username=user.username)
    if payment_user.is_student:
        return True
    else:
        return False


@login_required
def payment_option(request):
    if check_premium_status(request.user):
        return render(request, "payments/after_pay.html")

    return render(request, "payments/payment_option.html")


###  EC-pay use only
def ecpay_create_payment(request):
    request_user = request.user.username
    system_user = get_object_or_404(User, username=request_user)
    print(system_user.id)
    order = Order.objects.create(
        user_id=system_user.id,
        order_id=uuid.uuid4().hex[:20],  # 訂單號碼
        amount=600,  # 訂單金額
        status="pending",  # 訂單狀態
        payment_method="ecpay",  # 支付方式
        created_at=timezone.now(),
    )

    order_params = {
        "MerchantTradeNo": order.order_id,
        "MerchantTradeDate": order.created_at.strftime("%Y/%m/%d %H:%M:%S"),
        "PaymentType": "aio",
        "TotalAmount": order.amount,
        "TradeDesc": "TechEcho Premium",
        "ItemName": "升級成TechEcho Premium月訂閱用戶",
        "ReturnURL": "https://techecho.tonytests2.com/payments/ecpay_return/",
        "ChoosePayment": "Credit",
        "ClientBackURL": "https://techecho.tonytests.com/payments/ecpay_after_pay/",
        "OrderResultURL": "https://techecho.tonytests.com/payments/ecpay_after_pay/",
        "CustomField1": str(system_user.id),
        "CustomField2": "",
        "EncryptType": 1,
    }

    print(f"{order.order_id}")
    return HttpResponse(ecpay_api(order_params))


@csrf_exempt
def ecpay_return(request):
    if request.method == "POST":
        ecpay_payment_sdk = ECPayPaymentSdk(
            MerchantID=os.getenv("ECPAY_MerchantID"),
            HashKey=os.getenv("ECPAY_HashKey"),
            HashIV=os.getenv("ECPAY_HashIV"),
        )

        res = request.POST.dict()
        received_check_mac_value = request.POST.get("CheckMacValue")
        calculated_check_mac_value = ecpay_payment_sdk.generate_check_value(res)

        print(f'從綠界接收到的"CheckMacValue"為:{received_check_mac_value}')
        print(f'本地端計算出的"CheckMacValue"為:{calculated_check_mac_value}')

        if calculated_check_mac_value == received_check_mac_value:
            print("接收綠界回傳參數完整")
            order_id = request.POST.get("MerchantTradeNo")
            trade_status = request.POST.get("RtnCode")

            try:
                order = Order.objects.get(order_id=order_id)
                if trade_status == "1":
                    print("付款成功")
                    order.status = "paid"
                    print(f"{order.user_id}")
                    User.objects.filter(id=order.user_id).update(is_student="True")
                else:
                    order.status = "failed"
                    print("付款失敗")
                order.save()
                return HttpResponse("1|OK")
            except Order.DoesNotExist:
                print("找不到對應付款訂單")
                return HttpResponse("0|Order Not Found")
        else:
            print("CheckMacValue驗證失敗")
            return HttpResponse("0|CheckMacValue Error")


@csrf_exempt
def ecpay_after_pay(request):
    if request.method == "POST":
        return redirect("payments:ecpay_after_pay")
    else:
        return render(request, "payments/after_pay.html")


###  Line-pay use only
def linepay_create_payment(request):
    request_user = request.user.username
    system_user = get_object_or_404(User, username=request_user)
    order = Order.objects.create(
        user_id=system_user.id,
        order_id=uuid.uuid4().hex[:20],  # 訂單號碼
        amount=600,  # 訂單金額
        status="pending",  # 訂單狀態
        payment_method="linepay",  # 支付方式
        created_at=timezone.now(),
    )

    # Initialize the LINE Pay API client
    line_pay = LinePayApi(
        channel_id=os.getenv("LINE_PAY_CHANNEL_ID"),
        channel_secret=os.getenv("LINE_PAY_CHANNEL_SECRET"),
        is_sandbox=True,  # Set to False for production
    )

    # Set up the payment request payload for LINE Pay
    payload = {
        "amount": order.amount,
        "currency": "TWD",
        "orderId": order.order_id,
        "packages": [
            {
                "id": "package_id",
                "amount": "600",
                "name": "TechEcho Premium",
                "products": [
                    {
                        "name": "TechEcho Premium",
                        "quantity": 1,
                        "price": order.amount,
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
        print(response)

        if response["returnCode"] == "0000":
            # Save transaction ID to the payment object
            order.transaction_id = response["info"]["transactionId"]
            # order.order_id = response["info"]["orderId"]
            order.save()

            # Redirect the user to the LINE Pay payment page
            return redirect(response["info"]["paymentUrl"]["web"])
        else:
            order.status = "failed"
            return render(
                request,
                "payments/payment_error.html",
                {"error": response["returnMessage"]},
            )
    except Exception as e:
        return render(request, "payments/payment_error.html", {"error": str(e)})


def create_line_pay_headers(body, uri):

    nonce = secrets.token_hex(16)
    LINE_PAY_CHANNEL_SECRET = os.getenv("LINE_PAY_CHANNEL_SECRET")
    body_to_json = json.dumps(body)
    message = LINE_PAY_CHANNEL_SECRET + uri + body_to_json + nonce

    binary_message = message.encode()
    binary_LINE_PAY_CHANNEL_SECRET = LINE_PAY_CHANNEL_SECRET.encode()

    hash = hmac.new(binary_LINE_PAY_CHANNEL_SECRET, binary_message, hashlib.sha256)
    signature = base64.b64encode(hash.digest()).decode()

    headers = {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": os.getenv("LINE_PAY_CHANNEL_ID"),
        "X-LINE-Authorization-Nonce": nonce,
        "X-LINE-Authorization": signature,
    }
    return headers


def linepay_confirm_payment(request):
    transaction_id = request.GET.get("transactionId")
    order_id = request.GET.get("orderId")
    order = Order.objects.get(order_id=order_id)

    uri = f"{os.getenv('LINE_PAY_API_ENDPOINT')}/v3/payments/{transaction_id}/confirm"
    payload = {
        "amount": 600,  # 需確保這與創建訂單時的金額一致
        "currency": "TWD",  # 需確保這與創建訂單時的貨幣一致
    }
    signature_uri = f"/v3/payments/{transaction_id}/confirm"
    headers = create_line_pay_headers(payload, signature_uri)
    body = json.dumps(payload)

    response = requests.post(uri, headers=headers, data=body)

    print(response.status_code)
    print(response.text)

    result = response.json()
    print(result)

    print(order_id)
    print(order.order_id)
    if response.status_code == 200 and result.get("returnCode") == "0000":
        # 更新訂單狀態，例如：
        order.status = "paid"
        order.save()
        User.objects.filter(id=order.user_id).update(is_student="True")
    else:
        order.status = "failed"
        order.save()
        print("Line Payment confirmation failed.")

    return render(request, "payments/after_pay.html")


def linepay_cancel_payment(request):
    return HttpResponse("Payment canceled!")


###  Internal/Admin use only
@login_required
def disable_premium(request):
    username = request.user.username
    User.objects.filter(username=username).update(is_student="False")
    payment_user = get_object_or_404(User, username=username)
    if payment_user.is_student:
        return HttpResponse(f"帳號{username} 取消Premium失敗")
    else:
        return HttpResponse(f"帳號{username} 取消Premium完成")


def delete_order(request):
    id = request.GET.get("id")
    order = get_object_or_404(Order, id=id)
    order.delete()
    return HttpResponse("Delete order done!!")


def update_order(request):
    order_id = request.GET.get("order_id")
    Order.objects.filter(order_id=order_id).update(status="pending")
    return HttpResponse("Update order done!!")
