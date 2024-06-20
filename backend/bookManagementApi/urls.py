from django.urls import path, include
from rest_framework import routers
from bookManagementApi.views import BookViewSet, AverageBookPriceView

router = routers.DefaultRouter()
router.register("books", BookViewSet, basename="book")
urlpatterns = [
    path("", include(router.urls)),
    path(
        "books/published/yearly-average-price/<int:year>",
        AverageBookPriceView.as_view(),
        name="published-book-yearly-average-price",
    ),
]
