from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

from lib.models import SoftDeleteModel
from questions.models import Question


class Answer(SoftDeleteModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(
        validators=[MinLengthValidator(1, "問題描述至少要一個字")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    votes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    vote_type = models.CharField(
        max_length=10, choices=[("upvote", "Upvote"), ("downvote", "downvote")]
    )

    class Meta:
        unique_together = ("user", "answer")  # 會員對每個答案只能投票一次
