from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from storages.backends.s3boto3 import S3Boto3Storage


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    name = models.CharField(max_length=255, default="default_value")
    slug = models.SlugField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        storage=S3Boto3Storage,
    )
    about = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    time = models.CharField(max_length=255, null=True, blank=True)
    introduce = models.TextField(null=True, blank=True)
    skill = models.CharField(max_length=255, null=True, blank=True)
    github_link = models.URLField(max_length=200, blank=True, null=True)

    def get_display_name(self):
        return self.nickname or self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{get_random_string(10)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_display_name()


class PasswordReset(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"密碼重置{self.user.username}"
