from django.db import models
from django.conf import settings

class Schedule(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_teacher': True})
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.teacher.name} - {self.start_time} to {self.end_time}"

class Appointment(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    
    def __str__(self):
        return f"Appointment for {self.student.name} - {self.schedule}"