from django.db import models


class Payment(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()
    currency = models.CharField(max_length=3)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    vip_plan = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.order_id
