from django.db import models
from djongo import models as mongo_models
from common.bases import Base
from bookManagementApi.managers import BookManager


class Book(Base):
    _id = mongo_models.ObjectIdField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    author = models.CharField(max_length=100, null=False, blank=False)
    published_date = models.DateField()
    genre = models.CharField(max_length=100, null=False, blank=False)
    # We use FloatField and additional validation due to mongo not support DecimalField
    price = models.FloatField()
    objects = BookManager()

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        db_table = "book"
