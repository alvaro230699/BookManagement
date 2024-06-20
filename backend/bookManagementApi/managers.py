from common.bases import BaseManager
from django.db.models import Avg


class BookManager(BaseManager):

    def get_ordered_books(self, **kwargs):
        return self.get_queryset().filter(**kwargs).order_by("-created_at")

    def get_average_price(self, **kwargs):
        return (
            self.get_queryset().filter(**kwargs).aggregate(Avg("price"))["price__avg"]
        )
