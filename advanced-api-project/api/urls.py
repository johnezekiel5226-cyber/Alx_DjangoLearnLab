from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    # List all books
    path('books/', BookListView.as_view(), name='book-list'),

    # Retrieve one book
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # Create
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # Update (THIS IS REQUIRED)
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),

    # Delete (THIS IS REQUIRED)
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
