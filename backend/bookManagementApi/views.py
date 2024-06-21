from rest_framework import viewsets, pagination, views
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from bookManagementApi.serializers import BookSerializer, AverageBookPriceSerializer
from bookManagementApi.models import Book
from bson import ObjectId
from bookManagementApi.utils import (
    get_book_publish_status_by_path,
    serialize_with_custom_serializer,
)
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from bookManagementApi.utils import (
    swagger_auto_schema_for_non_get_methods,
    get_book_delete_status_by_path,
)


class BookPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


@swagger_auto_schema_for_non_get_methods(BookSerializer)
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    pagination_class = BookPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        is_deleted = get_book_delete_status_by_path(self.request.path) == "deleted"
        if is_deleted:
            qs = Book.objects.get_deleted_books()
        else:
            qs = Book.objects.get_ordered_books()
        return qs

    def get_object(self):
        self.kwargs["pk"] = ObjectId(self.kwargs.get("pk"))
        return super().get_object()

    @swagger_auto_schema(
        operation_description="Retrieve average price of requested published year book",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="JWT token in 'Bearer <token>' format",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve average price of requested published year book",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="JWT token in 'Bearer <token>' format",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AverageBookPriceView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer = AverageBookPriceSerializer

    @swagger_auto_schema(
        operation_description="Retrieve average price of requested published year book",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="JWT token in 'Bearer <token>' format",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "year",
                openapi.IN_PATH,
                description="Year of the published books.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
    )
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
