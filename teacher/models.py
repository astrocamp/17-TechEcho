from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 連接User模型
    expertise = models.CharField(max_length=255)  # 專業能力
    resume = models.TextField(
        validators=[MinLengthValidator(150), MaxLengthValidator(500)]
    )  # 簡單自傳，長度限制
    created_at = models.DateTimeField(default=timezone.now)  # 新增時間
    rating = models.FloatField(
        default=0.0, validators=[MinLengthValidator(1.0), MaxLengthValidator(5.0)]
    )  # 評分，最低1.0最高5.0

    def __str__(self):
        return f"{self.user.username} - {self.expertise}"

    def get_average_rating(self):
        """
        導師平均分數
        """
        return self.rating
