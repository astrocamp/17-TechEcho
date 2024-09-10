from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    # for teacher
    path("teacher/", views.schedule, name="schedule"),
    path("teacher/new/", views.schedule_new, name="schedule_new"),
    path("teacher/<int:id>/edit/", views.schedule_edit, name="schedule_edit"),
    path("teacher/<int:id>/delete/", views.schedule_delete, name="schedule_delete"),
    path("teacher/status/", views.schedule_status, name="schedule_status"),
    # for student
    path("teacher/available/", views.schedule_available, name="schedule_available"),
    path("student/", views.appointment, name="appointment"),
    path("student/<int:id>/new/", views.appointment_new, name="appointment_new"),
    path("student/<int:id>/edit/", views.appointment_edit, name="appointment_edit"),
    path(
        "student/<int:id>/delete/", views.appointment_delete, name="appointment_delete"
    ),
]
