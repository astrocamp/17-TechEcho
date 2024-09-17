from datetime import timedelta

from django.conf import settings
from django.db import models


class TeacherSchedule(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"user__is_teacher": True},
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ["teacher", "start_time"]
        unique_together = (
            "teacher",
            "start_time",
        )  # 確保同一教師在同一時間段內只能有一個時間安排

    def save(self, *args, **kwargs):
        if self.start_time:
            self.end_time = self.start_time + timedelta(hours=1)  # 假設預設為1小時
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.teacher.get_display_name()} - {self.start_time} to {self.end_time}"
        )


class StudentReservation(models.Model):
    schedule = models.ForeignKey(TeacherSchedule, on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"user__is_student": True},
    )

    class Meta:
        ordering = ["schedule__teacher", "schedule__start_time"]

    def __str__(self):
        return f"Reservation for {self.student.username} - {self.schedule}"
