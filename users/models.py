from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    name = models.CharField(max_length=100)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    third_party = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.name
