import uuid

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.http import url_has_allowed_host_and_scheme

from answers.models import Answer
from blogs.models import Blog
from questions.models import Question
from reservations.models import StudentReservation, TeacherSchedule

from .forms import UserPhotoForm, UserProfileForm, UserPublicProfileForm, UsersForm
from .helper import send_forget_password_mail
from .models import PasswordReset, User


def register(request):
    if request.method == "POST":
        form = UsersForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            request.session["new_user"] = True
            messages.success(request, "註冊成功並已自動登入！")
            return redirect("index")
        else:
            if "username" in form.errors:
                messages.error(request, "帳號錯誤")
            if "password1" in form.errors:
                messages.error(request, "密碼錯誤")
            if "password2" in form.errors:
                messages.error(request, "密碼不一致")
    else:
        form = UsersForm()
    return render(request, "users/register.html", {"form": form})


def log_in(request):
    next_url = request.POST.get("next") or request.GET.get("next") or reverse("index")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
        next_url = reverse("index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "登入成功")
            return redirect(next_url)
        else:
            if "username" and "password1" in form.errors:
                messages.error(request, "登入失敗，帳號密碼錯誤或尚未註冊")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form, "next": next_url})


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

        password_reset, _ = PasswordReset.objects.get_or_create(user=user)
        password_reset.forget_password_token = uuid.uuid4()
        password_reset.save()

        send_forget_password_mail(user.email, profile.forget_password_token)
        messages.success(request, "重設密碼的郵件已發送。")
    else:
        messages.error(request, "找不到此帳號。")

        return redirect("users:forget_password")

    return render(request, "users/forget_password.html")


def change_password(request, token):
    try:
        password_reset = PasswordReset.objects.get(forget_password_token=token)
    except PasswordReset.DoesNotExist:
        messages.error(request, "無效")
        return redirect("users:login")

    user = password_reset.user

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()

            password_reset.forget_password_token = None
            password_reset.save()

            messages.success(request, "密碼已成功更改，請使用新密碼登入。")
            return redirect("users:login")
        else:
            messages.error(request, "密碼不匹配或為空。")
            return redirect("users:change_password", token=token)

    context = {"token": token, "user_id": user.id}
    return render(request, "users/change_password.html", context)


@login_required
def profile(request):

    drafts = Blog.objects.filter(author=request.user, is_draft=True).order_by(
        "-created_at"
    )
    blogs = Blog.objects.filter(author=request.user, is_draft=False).order_by(
        "-created_at"
    )

    questions = Question.objects.filter(user=request.user).order_by("-created_at")[:]
    answers = (
        Answer.objects.filter(user=request.user)
        .select_related("question", "user")
        .order_by("-created_at")[:]
    )
    reservations = StudentReservation.objects.filter(
        student=request.user
    ).select_related("schedule__teacher")
    schedules = TeacherSchedule.objects.filter(teacher=request.user).prefetch_related(
        "studentreservation_set__student"
    )
    context = {
        "user": request.user,
        "drafts": drafts,
        "questions": questions,
        "answers": answers,
        "blogs": blogs,
        "reservations": reservations,
        "schedules": schedules,
    }
    return render(request, "users/profile.html", context)


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        photo_form = UserPhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and photo_form.is_valid():
            form.save()
            photo_form.save()
            if "HX-Request" in request.headers:
                response = HttpResponse()
                response["HX-Redirect"] = reverse("users:profile")
                return response
            else:
                return redirect("users:profile")
        else:
            if "HX-Request" in request.headers:
                html = render_to_string(
                    "users/profile_edit.html",
                    {"form": form, "photo_form": photo_form},
                    request,
                )
                return HttpResponse(html)
            else:
                messages.error(request, "請更正以下錯誤。")
    else:
        form = UserProfileForm(instance=request.user)
        photo_form = UserPhotoForm(instance=request.user)

    return render(
        request, "users/profile_edit.html", {"form": form, "photo_form": photo_form}
    )


@login_required
def public_profile(request, id):
    user = get_object_or_404(User, pk=id)
    schedules = TeacherSchedule.objects.filter(teacher_id=id).order_by("start_time")

    if request.method == "POST":
        form = UserPublicProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:public_profile", id=id)
    else:
        form = UserPublicProfileForm(instance=user)

    context = {
        "form": form,
        "user": user,
        "schedules": schedules,
    }
    return render(request, "users/public_profile.html", context)


def public_profile_edit(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == "POST":
        form = UserPublicProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:public_profile", id=id)
    else:
        form = UserPublicProfileForm(instance=user)

    return render(
        request, "users/public_profile_edit.html", {"form": form, "user": user}
    )
