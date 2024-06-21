from django.test import TestCase
from rest_framework.test import APIClient
from bookManagementApi.models import Book
from bookManagementApi.utils import get_json_response_from_client


class BookViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.get_books_url = "/api/books/"
        self.get_yearly_avg_price_url = (
            "/api/books/published/yearly-average-price/{year}"
        )

    def tearDown(self) -> None:
        Book.objects.all().delete()
        Book.objects.get_deleted_connections().delete()
        return super().tearDown()

    def test_get_books(self):
        self.tearDown()
        Book.objects.create(
            title="test_title",
            author="test_author",
            published_date="2024-06-01",
            genre="test_genre",
            price=12.05,
        )
        response = self.client.get(self.get_books_url)
        json_result = get_json_response_from_client(response.content)
        data = json_result["results"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_result["count"], 1)
        self.assertEqual(data[0]["title"], "test_title")
        self.assertEqual(data[0]["author"], "test_author")
        self.assertEqual(data[0]["published_date"], "2024-06-01")
        self.assertEqual(data[0]["genre"], "test_genre")
        self.assertEqual(data[0]["price"], 12.05)

    def test_get_yearly_avg_price_books(self):
        self.tearDown()
        test_year = 2024
        Book.objects.create(
            title="test_title",
            author="test_author",
            published_date=f"{test_year}-06-01",
            genre="test_genre",
            price=1,
        )
        Book.objects.create(
            title="test_title_2",
            author="test_author_2",
            published_date=f"{test_year}-06-01",
            genre="test_genre",
            price=3,
        )
        Book.objects.create(
            title="test_title_3",
            author="test_author_3",
            published_date=f"{test_year}-06-01",
            genre="test_genre",
            price=3,
        )
        response = self.client.get(self.get_yearly_avg_price_url.format(year=test_year))
        json_result = get_json_response_from_client(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_result["year"], 2024)
        self.assertEqual(json_result["average_price"], "2.33")
