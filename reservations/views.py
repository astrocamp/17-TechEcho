import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from chat.models import ChatGroup
from lib.utils.student_required import student_required
from lib.utils.teacher_required import teacher_required

from .forms import TeacherScheduleForm
from .models import StudentReservation, TeacherSchedule


# for teacher to set up schedule
@login_required
@teacher_required
def teacher_index(request):
    if request.method == "POST":
        form = TeacherScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.teacher = request.user
            if TeacherSchedule.objects.filter(
                teacher=schedule.teacher, start_time=schedule.start_time
            ).exists():
                messages.error(request, "此時間已經存在，無法重複新增")
                return render(
                    request, "reservations/teacher/teacher_new.html", {"form": form}
                )
            schedule.save()
            messages.success(request, "新增成功")
            return redirect("reservations:teacher_index")
        return render(request, "reservations/teacher/teacher_new.html", {"form": form})
    schedules = TeacherSchedule.objects.filter(teacher=request.user).prefetch_related(
        "studentreservation_set__student"
    )
    return render(
        request,
        "reservations/teacher/teacher_index.html",
        {
            "schedules": schedules,
            "teacher": request.user,
        },
    )


@login_required
@teacher_required
def teacher_new(request):
    form = TeacherScheduleForm()
    return render(request, "reservations/teacher/teacher_new.html", {"form": form})


@login_required
@teacher_required
def teacher_edit(request, id):
    schedule = get_object_or_404(TeacherSchedule, id=id)
    if schedule.studentreservation_set.exists():
        messages.error(request, "此時間已被預約，無法編輯")
        return redirect("reservations:teacher_index")
    if request.method == "POST":
        form = TeacherScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            if TeacherSchedule.objects.filter(
                teacher=schedule.teacher, start_time=schedule.start_time
            ).exists():
                messages.error(request, "此時間已經存在，請選擇其他時間")
                return render(
                    request, "reservations/teacher/teacher_new.html", {"form": form}
                )
            form.save()
            messages.success(request, "編輯成功")
            return redirect("reservations:teacher_index")
        return render(request, "reservations/teacher/teacher_edit.html", {"form": form})
    form = TeacherScheduleForm(instance=schedule)
    return render(
        request,
        "reservations/teacher/teacher_edit.html",
        {"schedule": schedule, "form": form},
    )


@login_required
@teacher_required
@require_POST
def teacher_delete(request, id):
    schedule = get_object_or_404(TeacherSchedule, id=id)
    if schedule.studentreservation_set.exists():
        message = "此時間已被預約，無法刪除"
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "error", "message": message})
        messages.error(request, message)
    else:
        schedule.delete()
        message = "刪除成功"
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "success", "message": message})
        messages.success(request, message)
    return redirect("reservations:teacher_index")


# for student to make reservations
@login_required
@student_required
def student_index(request):
    reservations = StudentReservation.objects.filter(
        student=request.user
    ).select_related("schedule__teacher")
    return render(
        request,
        "reservations/student/student_index.html",
        {"reservations": reservations},
    )


@login_required
@student_required
def student_new(request, id):
    schedule = get_object_or_404(
        TeacherSchedule.objects.exclude(teacher=request.user), id=id
    )

    if request.method == "POST":
        if StudentReservation.objects.filter(schedule=schedule).exists():
            messages.error(request, "不能預約重複時間")
            return redirect("reservations:student_new", id=id)

        s = StudentReservation.objects.create(schedule=schedule, student=request.user)
        messages.success(request, "預約成功")
        return redirect("reservations:student_index")
    return render(
        request, "reservations/student/student_new.html", {"schedule": schedule}
    )


@login_required
@student_required
def student_edit(request, id):
    reservation = get_object_or_404(StudentReservation, id=id)
    teacher_available = TeacherSchedule.objects.filter(
        studentreservation__isnull=True
    ).exclude(id=reservation.schedule.id)
    if request.method == "POST":
        new_schedule_id = request.POST.get("schedule_id")
        new_schedule = get_object_or_404(TeacherSchedule, id=new_schedule_id)
        reservation.schedule = new_schedule
        reservation.save()
        messages.success(request, "預約更新成功")
        return redirect("reservations:student_index")
    return render(
        request,
        "reservations/student/student_edit.html",
        {
            "reservation": reservation,
            "teacher_available": teacher_available,
        },
    )


@login_required
@student_required
def student_delete(request, id):
    reservation = get_object_or_404(StudentReservation, id=id)
    reservation.delete()
    messages.success(request, "取消預約成功")
    return redirect("reservations:student_index")


def teacher_available(request):
    if request.user.is_authenticated:
        schedules = (
            TeacherSchedule.objects.exclude(teacher=request.user)
            .filter(studentreservation__isnull=True)
            .select_related("teacher")
        )
    else:
        schedules = TeacherSchedule.objects.filter(
            studentreservation__isnull=True
        ).select_related("teacher")

    return render(
        request, "reservations/teacher/teacher_available.html", {"schedules": schedules}
    )


def calendar_events(request, teacher_id):
    schedules = TeacherSchedule.objects.filter(teacher=teacher_id).prefetch_related(
        "studentreservation_set__student"
    )
    events = [
        {
            "id": schedule.id,
            "title": (
                f"{schedule.studentreservation_set.first().student.get_display_name()}已預約"
                if schedule.studentreservation_set.exists()
                else ""
            ),
            "start": schedule.start_time.isoformat(),
            "end": schedule.end_time.isoformat(),
            "url": reverse("reservations:teacher_delete", args=[schedule.id]),
            "reserved": schedule.studentreservation_set.exists(),
        }
        for schedule in schedules
    ]
    return JsonResponse(events, safe=False)


@login_required
@teacher_required
def update_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event_id = data.get("id")
        start_time = data.get("start")
        end_time = data.get("end")

        schedule = get_object_or_404(TeacherSchedule, id=event_id, teacher=request.user)

        # 檢查事件是否已被預約
        if schedule.studentreservation_set.exists():
            return JsonResponse(
                {"status": "error", "message": "此時間已被預約，無法編輯"}, status=400
            )

        # 檢查事件是否更新到今天之前
        new_start_time = timezone.datetime.fromisoformat(start_time)
        if new_start_time < timezone.now():
            return JsonResponse(
                {"status": "error", "message": "無法移動到過去時間，請重新選擇"},
                status=400,
            )

        schedule = get_object_or_404(TeacherSchedule, id=event_id, teacher=request.user)
        schedule.start_time = timezone.datetime.fromisoformat(start_time)
        schedule.end_time = timezone.datetime.fromisoformat(end_time)
        schedule.save()

        return JsonResponse({"status": "success", "message": "時間更新成功！"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
