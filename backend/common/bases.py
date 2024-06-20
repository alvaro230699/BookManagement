from django.db import models
from django.utils import timezone


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(editable=False, null=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(Base, self).delete()


class BaseManager(models.Manager):
    def _get_all_connections(self):
        return super().get_queryset()

    def _get_queryset(self):
        return self._get_all_connections().filter(deleted_at=None)

    def get_queryset(self):
        return self._get_queryset()

    def get_deleted_connections(self, **kwargs):
        return (
            self._get_all_connections()
            .filter(deleted_at__isnull=False)
            .order_by("-deleted_at")
        )
