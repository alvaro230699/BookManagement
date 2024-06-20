from rest_framework import viewsets, pagination, views
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from bookManagementApi.serializers import BookSerializer, AverageBookPriceSerializer
from bookManagementApi.models import Book
from bson import ObjectId
from bookManagementApi.utils import (
    get_book_publish_status_by_path,
    serialize_with_custom_serializer,
)
from django.utils.translation import gettext_lazy as _


class BookPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        qs = Book.objects.get_ordered_books()
        return qs

    def get_object(self):
        self.kwargs["pk"] = ObjectId(self.kwargs.get("pk"))
        return super().get_object()


class AverageBookPriceView(views.APIView):
    # year_query_param = None
    year_query_description = _("Year of the published books.")
    serializer = AverageBookPriceSerializer

    def get(self, request, year):
        try:
            is_published = get_book_publish_status_by_path(request.path) == "published"
            filters = {}
            if is_published:
                filters["published_date__year"] = year
            average_price = Book.objects.get_average_price(**filters)
            if average_price is None:
                return Response(
                    {"error": "No books found for the given year"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serialized_response = serialize_with_custom_serializer(
                self.serializer, year=year, average_price=average_price
            )
            return Response(serialized_response, status=status.HTTP_200_OK)
        except AssertionError as e:
            Response(
                {"error": f"Bad request, please check the following log: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            Response(
                {"error": f"Following error happened: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
