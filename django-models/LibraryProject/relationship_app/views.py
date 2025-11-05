from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# --- Function-based view using template ---
def book_list(request):
    """
    List all books and their authors in HTML.
    """
    books = Book.objects.all()  # ✅ Query all books
    return render(request, 'relationship_app/list_books.html', {'books': books})  # ✅ Use the template


# --- Class-based view for library details ---
class LibraryDetailView(DetailView):
    """
    Display a specific library and all books in it.
    """
    model = Library
    context_object_name = 'library'
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()  # Books in this library
        return context
