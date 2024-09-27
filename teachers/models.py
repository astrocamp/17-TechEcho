from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from taggit.managers import TaggableManager


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    labels = TaggableManager()
    introduce = models.TextField(
        validators=[MinLengthValidator(50), MaxLengthValidator(500)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.user.is_teacher = True
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_display_name()}"
