import os
import django

# --- Setup Django environment manually so this can run standalone ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


# 1️⃣ Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author.name}:")
        for book in books:
            print(f" - {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with the name '{author_name}'.")


# 2️⃣ List all books in a library
def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library.name} library:")
        for book in books:
            print(f" - {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"No library found with the name '{library_name}'.")


# 3️⃣ Retrieve the librarian for a library (explicit query)
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # ✅ explicit query
        print(f"Librarian for {library.name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library found with the name '{library_name}'.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")


# -----------------------------
# Run sample queries
# -----------------------------
if __name__ == "__main__":
    # Change these to match actual data in your DB
    get_books_by_author("J.K. Rowling")
    print("-" * 40)
    list_books_in_library("Central Library")
    print("-" * 40)
    get_librarian_for_library("Central Library")
