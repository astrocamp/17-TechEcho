from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class User(AbstractUser):

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    name = models.CharField(max_length=255, default="default_value")
    slug = models.SlugField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)


def save(self, *args, **kwargs):
    if not self.slug:
        base_slug = slugify(self.name)
        self.slug = f"{base_slug}-{get_random_string(10)}"
    super().save(*args, **kwargs)


def __str__(self):
    return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
