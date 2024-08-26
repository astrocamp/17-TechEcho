from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    class Meta:
        abstract: True


class Question(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField(min_length=20)
    expectations = models.TextField(min_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    like = models.ManyToManyField(User, related_name="likes")
    follow = models.ManyToManyField(User, related_name="follows")

    def __str__(self):
        return self.title
