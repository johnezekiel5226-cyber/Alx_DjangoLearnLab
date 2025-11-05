from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library


# --- Function-based view (from before) ---
def book_list(request):
    """Lists all books and their authors as plain text."""
    books = Book.objects.select_related('author').all()

    if not books.exists():
        return HttpResponse("No books found in the database.")

    response_lines = ["List of Books:\n"]
    for book in books:
        response_lines.append(f"- {book.title} by {book.author.name}")

    response_text = "\n".join(response_lines)
    return HttpResponse(response_text, content_type="text/plain")


# --- Class-based view ---
class LibraryDetailView(DetailView):
    """
    Displays details for a specific library and lists all books available in that library.
    URL pattern should pass 'pk' or 'id' for the library.
    """
    model = Library
    context_object_name = 'library'
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        """Add all books in this library to the context."""
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.select_related('author').all()
        return context
