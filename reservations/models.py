from django.conf import settings
from django.db import models


class TeacherSchedule(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_teacher": True},
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.teacher} - {self.start_time} to {self.end_time}"


class StudentReservation(models.Model):
    schedule = models.ForeignKey(TeacherSchedule, on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"is_student": True},
    )

    def __str__(self):
        return f"Reservation for {self.student.username} - {self.schedule}"
