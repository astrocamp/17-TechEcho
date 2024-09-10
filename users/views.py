import logging
import uuid

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render, reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import UsersForm
from .helper import send_forget_password_mail
from .models import Profile, User

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = UsersForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session["new_user"] = True
            messages.success(request, "註冊成功並已自動登入！")
            return redirect("index")
        else:
            if "username" in form.errors:
                for error in form.errors["username"]:
                    messages.error(request, "帳號錯誤")
            if "email" in form.errors:
                for error in form.errors["email"]:
                    messages.error(request, "信箱已註冊過，或格式不正確")
            if "password1" in form.errors:
                for error in form.errors["password1"]:
                    messages.error(request, "密碼錯誤")
            if "password2" in form.errors:
                for error in form.errors["password2"]:
                    messages.error(request, "密碼不一致")
    else:
        form = UsersForm()
    return render(request, "layouts/register.html", {"form": form})


def log_in(request):
    next_url = request.POST.get("next") or request.GET.get("next") or reverse("index")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
        next_url = reverse("index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "登入成功")
            return redirect(next_url)
        else:
            messages.error(request, "登入失敗，帳號或密碼錯誤")
    else:
        form = AuthenticationForm()

    return render(request, "layouts/login.html", {"form": form, "next": next_url})


def log_out(request):
    logout(request)
    messages.success(request, "登出成功")
    return redirect("index")


def forget_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.filter(username=username).first()

        if not user:
            messages.error(request, "找不到此帳號。")
            return redirect("users:forget_password")

        profile, created = Profile.objects.get_or_create(user=user)
        profile.forget_password_token = uuid.uuid4()
        profile.save()

        send_forget_password_mail(user.email, profile.forget_password_token)
        messages.success(request, "重設密碼的郵件已發送。")
    else:
        messages.error(request, "找不到此帳號。")

        return redirect("users:forget_password")

    return render(request, "layouts/forget_password.html")


logger = logging.getLogger(__name__)


def change_password(request, token):
    logger.debug(f"Received change password request with token: {token}")

    try:
        profile = Profile.objects.get(forget_password_token=token)
    except Profile.DoesNotExist:
        logger.error(f"No profile found for token: {token}")
        messages.error(request, "無效的密碼重置令牌")
        return redirect("users:login")

    user = profile.user

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()

            profile.forget_password_token = None
            profile.save()

            messages.success(request, "密碼已成功更改，請使用新密碼登入。")
            return redirect("users:login")
        else:
            messages.error(request, "密碼不匹配或為空。")
            return redirect("users:change_password", token=token)

    context = {"token": token, "user_id": user.id}
    return render(request, "layouts/change_password.html", context)


def profile(request):
    return render(request, "layouts/profile.html")
