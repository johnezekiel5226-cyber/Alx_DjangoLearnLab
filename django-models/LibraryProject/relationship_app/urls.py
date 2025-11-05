from django.urls import path
from .views import book_list, LibraryDetailView

urlpatterns = [
    # Function-based view → list all books
    path('books/', book_list, name='book_list'),

    # Class-based view → show details for a specific library (by ID)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
