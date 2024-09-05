# allow user to delete
# but retain the record for a designated time frame
from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(deleted_at=None)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(default=None, null=True)

    objects = SoftDeleteManager()
    soft_deleted_objects = DeletedManager()
    all_objects = models.Manager()

    def delete(self, soft=True):
        if soft:
            self.deleted_at = timezone.now()
            self.save()
        else:
            super().delete()

    def revive(self):
        self.deleted_at = None
        self.save()

    def is_soft_deleted(self):
        return self.deleted_at is not None

    class Meta:
        abstract = True


def get_soft_delete_model(baseModel=models.Model):
    return SoftDeleteModel(baseModel)
