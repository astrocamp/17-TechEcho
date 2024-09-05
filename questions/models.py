from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from taggit.managers import TaggableManager

from lib.models import SoftDeleteModel


class Question(SoftDeleteModel):
    title = models.CharField(max_length=50)
    details = models.TextField(
        validators=[
            MinLengthValidator(20, "the field must contain at least 20 characters")
        ]
    )

    votes_count = models.IntegerField(default=0)

    answers_count = models.PositiveIntegerField(default=0)
    follows_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvotes")
    downvote = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="downvotes"
    )
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="follows")

    labels = TaggableManager()

    def __str__(self):
        return self.title
