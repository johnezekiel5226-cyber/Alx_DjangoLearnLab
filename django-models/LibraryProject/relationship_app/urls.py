from django.urls import path
from .views import book_list, LibraryDetailView
from .views import list_books
urlpatterns = [
    # Function-based view → list all books
    path('books/', book_list, name='book_list'),

    # Class-based view → show details for a specific library (by ID)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
