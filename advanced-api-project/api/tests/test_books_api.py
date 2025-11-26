# api/tests/test_books_api.py

import pytest
from django.urls import reverse
from api.models import Book
from api.tests.helpers import get_auth_client


@pytest.mark.django_db
def test_create_book():
    client, user = get_auth_client()
    url = reverse('book-list')  # or 'books:create' depending on your router

    data = {
        'title': 'New Book',
        'author': 'John Doe'
    }

    response = client.post(url, data)

    assert response.status_code == 201
    assert Book.objects.count() == 1
    assert response.data['title'] == 'New Book'


@pytest.mark.django_db
def test_list_books():
    client, user = get_auth_client()

    # Create sample books
    Book.objects.create(title='Book A', author='Author A')
    Book.objects.create(title='Book B', author='Author B')

    url = reverse('book-list')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_retrieve_book():
    client, user = get_auth_client()

    book = Book.objects.create(title='Test Book', author='Test Author')

    url = reverse('book-detail', args=[book.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data['title'] == 'Test Book'


@pytest.mark.django_db
def test_update_book():
    client, user = get_auth_client()

    book = Book.objects.create(title='Old Title', author='Old Author')

    url = reverse('book-detail', args=[book.id])
    data = {'title': 'Updated Title', 'author': 'Updated Author'}

    response = client.put(url, data)

    book.refresh_from_db()

    assert response.status_code == 200
    assert book.title == 'Updated Title'


@pytest.mark.django_db
def test_delete_book():
    client, user = get_auth_client()

    book = Book.objects.create(title='Delete Me', author='Anon')

    url = reverse('book-detail', args=[book.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert Book.objects.count() == 0

@pytest.mark.django_db
def test_create_book_requires_authentication(client):
    url = reverse('book-list')

    response = client.post(url, {
        'title': 'Unauthorized Book',
        'author': 'Nobody'
    })

    assert response.status_code == 401  # or 403 depending on your permission class
