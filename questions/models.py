from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from taggit.managers import TaggableManager

from lib.models import SoftDeleteModel


class Question(SoftDeleteModel):
    title = models.CharField(max_length=50)
    details = models.TextField(
        validators=[MinLengthValidator(20, "問題描述至少要二十個字")]
    )

    votes_count = models.IntegerField(default=0)
    answers_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="votes", through="QuestionUserVotes"
    )
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="follows")

    labels = TaggableManager()

    def __str__(self):
        return self.title

    def followed_by(self, user) -> bool:
        return self.followers.filter(id=user.id).exists()

    def has_voted(self, user) -> bool:
        return self.voters.filter(id=user.id).exists()


class QuestionUserVotes(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_status = models.CharField(max_length=10, default="neither")

    def __str__(self) -> str:
        return f"question:{self.question.title} was voted {self.vote_status} by user:{self.user}"
