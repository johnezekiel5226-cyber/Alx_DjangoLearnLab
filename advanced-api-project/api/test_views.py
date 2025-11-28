"""
api/test_views.py

Comprehensive unit tests for the Book API endpoints.

Run with:
    python manage.py test api

Assumptions:
- You have a Book model with at least: title (CharField) and author (CharField).
- Your DRF router/register created URL names 'book-list' and 'book-detail'.
  (Common when using DefaultRouter with basename='book' or viewset named BookViewSet.)
- Authentication may be required for create/update/delete. Tests accept either 401 or 403
  for unauthenticated attempts where appropriate.
"""

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from api.models import Book


User = get_user_model()


def create_user_and_client(username="testuser", password="testpass"):
    """Create a user and return an APIClient authenticated as that user."""
    user = User.objects.create_user(username=username, password=password)
    client = APIClient()
    # use force_authenticate so test doesn't depend on token/session setup
    client.force_authenticate(user=user)
    return user, client


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Unauthenticated client (for tests that check unauthenticated access)
        self.anon_client = APIClient()

        # Authenticated user + client
        self.user, self.client = create_user_and_client()

        # Base URL names (adjust if your router uses different names)
        self.list_url = reverse("book-list")
        # detail URL reversed with id in tests as needed

        # Create some sample books
        Book.objects.create(title="Alpha", author="Author A")
        Book.objects.create(title="Beta", author="Author B")
        Book.objects.create(title="Gamma", author="Author A")  # duplicate author for filtering

    # -------------------------
    # CRUD Tests
    # -------------------------
    def test_list_books(self):
        """List endpoint returns all books (200)."""
        resp = self.anon_client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # expect at least the 3 created in setUp
        # DRF list responses commonly return a list or paginated results; handle both.
        if isinstance(resp.data, dict) and "results" in resp.data:
            count = len(resp.data["results"])
        else:
            count = len(resp.data)
        self.assertGreaterEqual(count, 3)

    def test_retrieve_book(self):
        """Retrieve single book by id."""
        book = Book.objects.first()
        detail_url = reverse("book-detail", args=[book.pk])
        resp = self.anon_client.get(detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("title"), book.title)

    def test_create_book_requires_authentication(self):
        """Unauthenticated create should be rejected (401 or 403)."""
        data = {"title": "New Book", "author": "Author X"}
        resp = self.anon_client.post(self.list_url, data)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated user can create a book (201) and data saved."""
        data = {"title": "Created by Test", "author": "Tester"}
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Confirm created in DB
        self.assertTrue(Book.objects.filter(title="Created by Test", author="Tester").exists())

    def test_update_book_requires_authentication(self):
        """Unauthenticated update should be rejected (401 or 403)."""
        book = Book.objects.first()
        detail_url = reverse("book-detail", args=[book.pk])
        data = {"title": "Hacked Title", "author": book.author}
        resp = self.anon_client.put(detail_url, data)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        """Authenticated user can update a book (200) and changes persist."""
        book = Book.objects.first()
        detail_url = reverse("book-detail", args=[book.pk])
        data = {"title": "Updated Title", "author": "Updated Author"}
        resp = self.client.put(detail_url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, "Updated Title")
        self.assertEqual(book.author, "Updated Author")

    def test_partial_update_book_authenticated(self):
        """Authenticated user can partial-update (PATCH)."""
        book = Book.objects.first()
        detail_url = reverse("book-detail", args=[book.pk])
        resp = self.client.patch(detail_url, {"title": "Partially Updated"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, "Partially Updated")

    def test_delete_book_requires_authentication(self):
        """Unauthenticated delete should be rejected (401 or 403)."""
        book = Book.objects.first()
        detail_url = reverse("book-detail", args=[book.pk])
        resp = self.anon_client.delete(detail_url)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book (204) and it is removed."""
        book = Book.objects.create(title="To be deleted", author="Delete Me")
        detail_url = reverse("book-detail", args=[book.pk])
        resp = self.client.delete(detail_url)
        # Accept 204 No Content for successful deletion
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=book.pk).exists())

    # -------------------------
    # Filtering / Searching / Ordering Tests
    # -------------------------
    def test_filter_by_author(self):
        """Filter books by author returns only matching items."""
        resp = self.anon_client.get(self.list_url, {"author": "Author A"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # parse list / pagination
        if isinstance(resp.data, dict) and "results" in resp.data:
            items = resp.data["results"]
        else:
            items = resp.data
        # All returned should have author == "Author A"
        for item in items:
            self.assertEqual(item.get("author"), "Author A")

    def test_search_title_partial_match(self):
        """
        If search is configured via DRF SearchFilter (search_fields),
        a query like ?search=Alp should match "Alpha".
        """
        resp = self.anon_client.get(self.list_url, {"search": "Alp"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        if isinstance(resp.data, dict) and "results" in resp.data:
            items = resp.data["results"]
        else:
            items = resp.data
        titles = [i.get("title") for i in items]
        self.assertTrue(any("Alpha" == t or "Alpha" in t for t in titles))

    def test_ordering_by_title_asc_and_desc(self):
        """Test ordering by title ascending and descending using ?ordering=title / -title"""
        # Ascending
        resp_asc = self.anon_client.get(self.list_url, {"ordering": "title"})
        self.assertEqual(resp_asc.status_code, status.HTTP_200_OK)
        if isinstance(resp_asc.data, dict) and "results" in resp_asc.data:
            items_asc = resp_asc.data["results"]
        else:
            items_asc = resp_asc.data
        titles_asc = [i.get("title") for i in items_asc]
        # Descending
        resp_desc = self.anon_client.get(self.list_url, {"ordering": "-title"})
        self.assertEqual(resp_desc.status_code, status.HTTP_200_OK)
        if isinstance(resp_desc.data, dict) and "results" in resp_desc.data:
            items_desc = resp_desc.data["results"]
        else:
            items_desc = resp_desc.data
        titles_desc = [i.get("title") for i in items_desc]

        # If at least 2 items, titles_asc should be reverse of titles_desc
        if len(titles_asc) >= 2 and len(titles_desc) >= 2:
            self.assertEqual(titles_asc, list(reversed(titles_desc)))

    # -------------------------
    # Permission / Auth Behavior Tests (extra checks)
    # -------------------------
    def test_multiple_permission_behaviors(self):
        """
        Check that an authenticated user gets different status codes than anonymous
        for modify endpoints. This is a sanity test to ensure permissions are effective.
        """
        book = Book.objects.first()
        detail_url = reverse("book-detail", args=[book.pk])

        # anonymous should not be able to delete/update (401/403)
        anon_put = self.anon_client.put(detail_url, {"title": "X", "author": book.author})
        anon_delete = self.anon_client.delete(detail_url)
        self.assertIn(anon_put.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertIn(anon_delete.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticated should get 200/204 for same operations
        auth_put = self.client.put(detail_url, {"title": "Auth Update", "author": book.author})
        auth_delete = self.client.delete(detail_url)
        self.assertIn(auth_put.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        self.assertIn(auth_delete.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
