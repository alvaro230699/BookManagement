from django.db import transaction
from django.forms.models import model_to_dict
from rest_framework import serializers
from bookManagementApi.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate_price(self, value):
        if value >= 100000 or value < 0:
            raise serializers.ValidationError(
                "Price must be a positive number with up to 6 digits in total."
            )
        if len(str(value).split(".")[-1]) > 2:
            raise serializers.ValidationError("Price must have up to 2 decimal places.")
        return value


class AverageBookPriceSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    average_price = serializers.DecimalField(max_digits=6, decimal_places=2)

    @staticmethod
    def parse_to_serialize(year, average_price):
        return {"year": year, "average_price": average_price}
