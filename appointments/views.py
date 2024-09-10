from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Schedule, Appointment
from teachers.models import Teacher


# for teacher to set up schedule
@login_required
def schedule(request):
    if not request.user.is_teacher:
        messages.error(request, '您還不是老師')
        return redirect('teachers:mentor')
    schedules = Schedule.objects.filter(teacher=request.user)
    return render(request, 'appointments/schedule.html', {'schedules': schedules})

@login_required
def schedule_new(request):
    if not request.user.is_teacher:
        messages.error(request, '您還不是老師')
        return redirect('teachers:mentor')
    if request.method == 'POST':
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        Schedule.objects.create(teacher=request.user, start_time=start_time, end_time=end_time)
        messages.success(request, '新增成功')
        return redirect('appointments:schedule')
    return render(request, 'appointments/schedule_new.html')

@login_required
def schedule_edit(request, id):
    if not request.user.is_teacher:
        messages.error(request, '您還不是老師')
        return redirect('teachers:mentor')
    schedule = get_object_or_404(Schedule, id=id)
    if request.method == 'POST':
        schedule.start_time = request.POST['start_time']
        schedule.end_time = request.POST['end_time']
        schedule.save()
        messages.success(request, '編輯成功')
        return redirect('appointments:schedule')
    return render(request, 'appointments/schedule_edit.html', {'schedule': schedule})

@login_required
def schedule_delete(request, id):
    if not request.user.is_teacher:
        messages.error(request, '您還不是老師')
        return redirect('teachers:mentor')
    schedule = get_object_or_404(Schedule, id=id)
    schedule.delete()
    messages.success(request, '刪除成功')
    return redirect('appointments:schedule')

@login_required
def schedule_status(request):
    if not request.user.is_teacher:
        messages.error(request, '您還不是老師')
        return redirect('teachers:mentor')
    schedules = Schedule.objects.filter(teacher=request.user).prefetch_related('appointment_set')
    return render(request, 'appointments/schedule_status.html', {'schedules': schedules})



# for student to make appointments
@login_required
def appointment(request):
    if not request.user.is_student:
        messages.error(request, '您還不是學生')
        return redirect('teachers:index')
    appointments = Appointment.objects.filter(student=request.user)
    return render(request, 'appointments/appointment.html', {'appointments': appointments})

@login_required
def appointment_new(request, id):
    if not request.user.is_student:
        messages.error(request, '您還不是學生')
        return redirect('teachers:index')
    schedule = get_object_or_404(Schedule, id=id)
    if request.method == 'POST':
        if Appointment.objects.filter(schedule=schedule).exists():
            messages.error(request, '此時間已被預約')
            return redirect('appointments:schedule_available')
        appointment = Appointment.objects.create(schedule=schedule, student=request.user)
        messages.success(request, '預約成功')
        return redirect('appointments:appointment')
    return render(request, 'appointments/appointment_new.html', {'schedule': schedule})

@login_required
def appointment_edit(request, id):
    if not request.user.is_student:
        messages.error(request, '您還不是學生')
        return redirect('teachers:index')

    appointment = get_object_or_404(Appointment, id=id)
    schedule_available = Schedule.objects.exclude(appointment__isnull=False).exclude(id=appointment.schedule.id)
    if request.method == 'POST':
        new_schedule_id = request.POST.get('schedule_id')
        new_schedule = get_object_or_404(Schedule, id=new_schedule_id)

        if Appointment.objects.filter(schedule=new_schedule).exists():
            messages.error(request, '此時間已被預約')
            return redirect('appointments:schedule_available')
        
        appointment.schedule = new_schedule
        appointment.save()
        messages.success(request, '預約更新成功')
        return redirect('appointments:appointment')

    return render(request, 'appointments/appointment_edit.html', {
        'appointment': appointment,
        'schedule_available': schedule_available,
    })

@login_required
def appointment_delete(request, id):
    if not request.user.is_student:
        messages.error(request, '您還不是學生')
        return redirect('teachers:index')
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    messages.success(request, '取消預約成功')
    return redirect('appointments:appointment')

@login_required
def schedule_available(request):
    if not request.user.is_student:
        messages.error(request, '您還不是學生')
        return redirect('teachers:mentor')
    schedules = Schedule.objects.exclude(appointment__isnull=False)
    return render(request, 'appointments/schedule_available.html', {'schedules': schedules})