from urllib.parse import unquote

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from answers.models import Answer
from lib.utils.labels import parse_labels
from lib.utils.pagination import paginate
from questions.models import Question
from reservations.models import TeacherSchedule

from .forms import TeacherForm
from .models import Teacher


def mentor(request):
    if request.user.is_authenticated and request.user.is_teacher:
        teacher_name = request.user.nickname
        messages.success(request, f"歡迎 {teacher_name}")
        return redirect("teachers:show", request.user.teacher.id)
    return render(request, "teachers/mentor.html")


def index(request):
    label_filter = request.GET.get("label", None)
    search_query = request.GET.get("search", None)
    if search_query:
        search_query = search_query.strip()

    if request.method == "POST":
        # 檢查是否該使用者已經是專家
        if Teacher.objects.filter(user=request.user).exists():
            messages.error(request, "你已經註冊為專家，無法重複註冊")
            return redirect("teachers:index")
        form = TeacherForm(request.POST)
        labels = parse_labels(request.POST)

        if not labels:
            messages.error(request, "標籤至少要一個，且是認可的程式語言")
            return render(request, "teachers/new.html", {"form": form})
        nickname = request.POST.get("nickname", None)

        if nickname and form.is_valid():
            teacher_info = form.save(commit=False)
            teacher_info.user = request.user
            teacher_info.save()
            teacher_info.labels.set(labels)
            form.save_m2m()
            request.user.nickname = unquote(nickname)
            request.user.save()
            messages.success(request, "歡迎加入")
            return redirect("teachers:index")
        return render(request, "teachers/new.html", {"form": form})

    teachers = Teacher.objects.all().prefetch_related("labels").order_by("-updated_at")
    if label_filter:
        teachers = teachers.filter(labels__name__exact=label_filter)
    if search_query:
        teachers = teachers.filter(
            Q(user__nickname__icontains=search_query)
            | Q(user__username__icontains=search_query)
        )
    no_results = not teachers.exists()

    all_labels = sorted(set(teachers.values_list("labels__name", flat=True)))
    teachers = paginate(request, teachers, items_count=8)
    return render(
        request,
        "teachers/index.html",
        {
            "teachers": teachers,
            "all_labels": all_labels,
            "no_results": no_results,
        },
    )


@login_required
def new(request):
    if request.user.is_teacher:
        messages.error(request, "你已經註冊為專家，無法重複註冊")
        return redirect("teachers:show", request.user.teacher.id)
    form = TeacherForm()
    return render(request, "teachers/new.html", {"form": form})


def show(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == "POST":
        if request.user.is_anonymous or request.user.teacher.id != teacher.id:
            messages.error(request, "你沒有權限")
            return redirect("teachers:show", id=id)

        form = TeacherForm(request.POST, instance=teacher)
        labels = parse_labels(request.POST)

        if not labels:
            messages.error(request, "標籤至少要一個，且是認可的程式語言")
            return render(request, "teachers/new.html", {"form": form})

        nickname = request.POST.get("nickname", None)
        if nickname and form.is_valid():
            teacher_info = form.save(commit=False)  # 暫存資料，避免直接提交
            teacher_info.labels.set(labels)
            teacher_info.save()
            form.save_m2m()

            teacher.user.nickname = unquote(nickname)
            teacher.user.save()
            messages.success(request, "更新成功")
            return redirect("teachers:show", id=id)
        messages.error(request, "輸入資料錯誤，請再嘗試")
        return render(request, "teachers/edit.html", {"teacher": teacher, "form": form})

    questions = Question.objects.filter(user=teacher.user).order_by("-created_at")[:8]
    answers = (
        Answer.objects.filter(user=teacher.user)
        .select_related("question", "user")
        .order_by("-created_at")[:8]
    )
    schedules = TeacherSchedule.objects.filter(teacher=teacher.user).order_by(
        "start_time"
    )
    print(schedules)
    context = {
        "teacher": teacher,
        "questions": questions,
        "answers": answers,
        "schedules": schedules,
    }

    return render(request, "teachers/show.html", context)


@login_required
@require_POST
def edit(request, id):
    teacher = get_object_or_404(Teacher, id=id, user=request.user)
    form = TeacherForm(instance=teacher)
    return render(
        request,
        "teachers/edit.html",
        {"teacher": teacher, "form": form, "labels": teacher.labels.all()},
    )


@login_required
@require_POST
def delete(request, id):
    teacher = get_object_or_404(Teacher, id=id, user=request.user)
    teacher.user.is_teacher = False
    teacher.user.save()
    teacher.delete()
    messages.success(request, "刪除成功")
    return redirect("teachers:index")
