from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render


def register(request, id=None):
    if id:
        existing_user = get_object_or_404(User, pk=id)
    else:
        existing_user = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if not username or not password:
            messages.error(request, "必須填寫帳號跟密碼")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "此用戶名已存在")
        else:
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            user.save()
            messages.success(request, "註冊成功")
            return redirect("users:login", id=user.id)

    return render(request, "register.html", {"existing_user": existing_user})


def log_in(request, id=None):
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
            return redirect("pages")
        else:
            messages.error(request, "登入失敗")

    return render(request, "login.html", {"existing_user": existing_user})


def log_out(req):
    if req.method == "POST":
        logout(req)
        messages.success(req, "登出成功")
        return redirect("layout:base")
