from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField(
        validators=[
            MinLengthValidator(20, "the field must contain at least 20 characters")
        ]
    )
    expectations = models.TextField(
        validators=[
            MinLengthValidator(20, "the field must contain at least 20 characters")
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    like = models.ManyToManyField(User, related_name="likes")
    follow = models.ManyToManyField(User, related_name="follows")

    def __str__(self):
        return self.title
