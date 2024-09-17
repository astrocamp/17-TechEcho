from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from lib.utils.student_required import student_required
from lib.utils.teacher_required import teacher_required
from teachers.models import Teacher

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
            schedule.save()
            messages.success(request, "新增成功")
            return redirect("reservations:teacher_index")
        return render(request, "reservations/teacher/teacher_new.html", {"form": form})
    schedules = (
        TeacherSchedule.objects.filter(teacher=request.user)
        .prefetch_related("studentreservation_set")
        .order_by("start_time")
    )
    return render(
        request, "reservations/teacher/teacher_index.html", {"schedules": schedules}
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
def teacher_delete(request, id):
    schedule = get_object_or_404(TeacherSchedule, id=id)
    if schedule.studentreservation_set.exists():
        messages.error(request, "此時間已被預約，無法刪除")
        return redirect("reservations:teacher_index")
    schedule.delete()
    messages.success(request, "刪除成功")
    return redirect("reservations:teacher_index")


# for student to make reservations
@login_required
@student_required
def student_index(request):
    reservations = StudentReservation.objects.filter(student=request.user).order_by(
        "schedule__teacher", "schedule__start_time"
    )
    return render(
        request,
        "reservations/student/student_index.html",
        {"reservations": reservations},
    )


@login_required
@student_required
def student_new(request, id):
    schedule = get_object_or_404(TeacherSchedule, id=id)
    if request.method == "POST":
        StudentReservation.objects.create(schedule=schedule, student=request.user)
        messages.success(request, "預約成功")
        return redirect("reservations:student_index")
    return render(
        request, "reservations/student/student_new.html", {"schedule": schedule}
    )


@login_required
@student_required
def student_edit(request, id):
    reservation = get_object_or_404(StudentReservation, id=id)
    teacher_available = (
        TeacherSchedule.objects.filter(studentreservation__isnull=True)
        .exclude(id=reservation.schedule.id)
        .order_by("teacher", "start_time")
    )

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
    schedules = TeacherSchedule.objects.exclude(
        studentreservation__isnull=False
    ).order_by("teacher", "start_time")
    return render(
        request, "reservations/teacher/teacher_available.html", {"schedules": schedules}
    )
