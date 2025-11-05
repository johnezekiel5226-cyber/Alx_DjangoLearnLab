from django.shortcuts import render
from .models import Book

def book_list(request):
    """Render a list of all books and their authors in HTML."""
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})
