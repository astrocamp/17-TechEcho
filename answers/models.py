# from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models

from questions.models import Question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
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
