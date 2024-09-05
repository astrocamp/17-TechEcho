from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .models import User


def register(request, id=None):
    if id:
        existing_user = get_object_or_404(User, pk=id)
    else:
        existing_user = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exists():
            messages.error(request, "用戶名已存在")
            return render(
                request,
                "register.html",
            )
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email, name=username
            )
            return redirect("users:login")

    return render(request, "register.html")


def log_in(request, id=None):
    next_url = request.GET.get("next")
    if id:
        existing_user = get_object_or_404(User, pk=id)
    else:
        existing_user = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "登入成功！")  # 設置成功消息
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            return redirect("index")  # 或其他頁面
        else:
            messages.error(request, "登入失敗：用戶名或密碼不正確")

    return render(request, "login.html", {"existing_user": existing_user})


def log_out(request):
    messages.success(request, "登出成功")
    logout(request)
    return redirect("index")
